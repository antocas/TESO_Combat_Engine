# pylint: disable=line-too-long
""" Main for testing """
import json
import random
from src.models.dummy import Dummy
from src.models.character import Character
from src.models.attack import Attack
from src.models import combat_queue
from src.models.effects import Effect
from src.models.skill import Skill

def main_combat(character: Character, dummy: Dummy):
    """ Main simulation thread """
    with open('src/skills/light_attack.json', 'r', encoding='utf-8') as file:
        json_skill = json.load(file)
        load_light_attack = Skill(json_skill)
        for l_a in Attack.skill_to_attack(load_light_attack):
            light_attack = l_a
    queue = combat_queue.QueueAttack()
    seconds = 1000
    initial_health = dummy.health

    while dummy.health > 0:
        print('*******************', seconds//1000, '*******************')
        latest_skill = None
        queue.add_attack(light_attack)
        # Renovamos la rotacion
        for to_renovate in character.rotation:
            if not queue.in_queue(to_renovate.lower()):
                # Pasamos el nombre en minuscula
                latest_skill = character.get_skill(to_renovate)
                for attack in Attack.skill_to_attack(latest_skill):
                    queue.add_attack(attack)
                print('Añadido el ataque:', to_renovate)
                break


        # Ronda de debuffs
        dummy.apply_debuffs()
        # ! Ronda de inserción de nuevos debuffs
        for debuff in latest_skill.debuffs:
            # Hay que cargar los debuffs en un buffer desde los JSON para que esto sea medianamente rapido y agil, buen finde!
            try:
                debuff = Effect.open_as_effect(debuff.effect, 'debuff', debuff.duration)
                dummy.set_debuff(debuff)
            except AttributeError:
                continue
        character.apply_buffs()

        # Ronda de ataque
        total = 0
        for name, attack in queue.next_attack():
            if attack.can_be_used(seconds) and attack.causes_damage():
                index = int(name.split(' ')[-1])
                max_resource = max(int(character.max_magicka), int(character.max_stamina))
                resource_damage = max(int(character.spell_damage), int(character.weapon_damage))
                attack.calculate_damage(max_resource, resource_damage, index=index)
                attack.increase_damage(character.damage_done)

                critical = random.randint(0, 100) <= character.critical_chance//219.12
                if critical:
                    max_critical = max(character.spell_critical, character.weapon_critical)/100.0
                    attack.make_critical(max_critical)
                    attack.increase_damage(character.critical_damage_done)
                # Daño con penetracion de armadura
                received = dummy.hit_dummy(attack.value, int(character.spell_penetration), critical_damage=critical)
                total = total + received
                print(f"{attack}, DMG: {received}, Critical: {critical}")

            attack.decrease_attack_duration(seconds)
            if attack.duration <= 0:
                queue.remove_attack(name)
                print("Removed:", name)

        queue.clear_attacks()
        print("Dummy health:", dummy.health, "Total damage this round:", total)
        seconds = seconds + 1000

    seconds = seconds//1000
    combat_minutes = seconds//60
    combat_seconds = seconds%60
    return {"dps": initial_health//seconds, "total": seconds, "minutes": combat_minutes, "seconds": combat_seconds}
