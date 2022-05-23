# pylint: disable=line-too-long
""" Main for testing """
import random
from src.models.dummy import Dummy
from src.models.character import Character
from src.models.attack import Attack
from src.models import combat_queue

def main_combat(character: Character, dummy: Dummy):
    """ Main simulation thread """
    queue = combat_queue.QueueAttack()
    seconds = 0
    channeling_time = 1

    round = 1
    while dummy.health > 0:
        print('*******************', round, '*******************')

        # Renovamos la rotacion
        for to_renovate in character.rotation:
            if not queue.in_queue(to_renovate):
                skill = character.get_skill(to_renovate)
                for attack in Attack.skill_to_attack(skill):
                    queue.add_attack(attack)
                break

        # Ronda de debuffs


        # Ronda de ataque
        for name, attack in queue.next_attack():
            index = int(name.split(' ')[-1])
            max_resource = max(int(character.max_magicka), int(character.max_stamina))
            resource_damage = max(int(character.spell_damage), int(character.weapon_damage))
            attack.calculate_damage(max_resource, resource_damage, index=index)
            attack.decrease_attack_duration()

            # Daño con penetracion de armadura
            dummy.hit_dummy(attack.value, int(character.spell_penetration))

            if attack.duration <= 0:
                queue.remove_attack(name)

            print(name)

        queue.clear_attacks()
        print("Dummy health:", dummy.health)
        round = round + 1
    #     # DAMAGE = 5000
    #     crit_prob = character.spell_critical
    #     max_crit = character.spell_critical
    #     penetration = character.spell_penetration
    #     # penetration = 18200

    #     dummy.apply_debuffs()

    #     # RONDA DE ATAQUES
    #     for name, atk in queue.attacks.items():
    #         print(name)
    #         damage = atk.value
    #         if random.random() <= crit_prob:
    #             damage += damage*max_crit
    #         dummy.hit_dummy(damage, penetration)
    #         # TEST
    #         queue.decrease_attack_duration(atk.name, channeling_time)
    #     print('*'*200)
    #     dummy.reset_resistances()
    #     queue.clear_attacks()
    #     seconds = seconds + channeling_time

    # combat_minutes = seconds//60
    # combat_seconds = seconds%60
    # return {"total": seconds, "minutes": combat_minutes, "seconds": combat_seconds}
