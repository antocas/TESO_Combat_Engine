""" Main for testing """
import random
from src.mc.dummy import Dummy
from src.mc.character import Character
from src.mc import attack
from src.mc import combat_queue

from src.instances.model_attack import *

import streamlit as st

def main_combat(dummy:Dummy, character:Character):
    queue = combat_queue.QueueAttack()
    initial_health = dummy.health
    seconds = 0
    channeling_time = 1

    circular = [barbed_trap, wall_of_elements, mystic_orb, blazing_spear, degeneration, puncturing_sweep]
    dummy.set_debuff(minor_breach)

    while dummy.attributes["health_bar"] > 0:
        queue.add_attack(light_attack)
        for to_renovate in circular:
            if not queue.in_queue(to_renovate._name):
                # print(seconds, to_renovate._name)
                queue.add_attack(to_renovate)
                break
        
        # DAMAGE = 5000
        CRIT_PROB = character.spell_critical
        MAX_CRIT = character.spell_critical
        PENETRATION = character.spell_penetration
        # PENETRATION = 18200

        dummy.apply_debuffs()
        
        # RONDA DE ATAQUES
        for name, attack in queue._attacks.items():
            print(name)
            DAMAGE = attack._value
            if random.random() <= CRIT_PROB:
                DAMAGE += DAMAGE*MAX_CRIT
            dummy.hit_dummy(DAMAGE, PENETRATION)
            # TEST
            queue.decrease_attack_duration(attack._name, channeling_time)
        print('*'*200)
        dummy.reset_resistances()
        queue.clear_attacks()
        seconds = seconds + channeling_time

    combat_minutes = seconds//60
    combat_seconds = seconds%60
    
    st.session_state['dps'] = initial_health//seconds
    st.session_state['time_minutes'] = combat_minutes
    st.session_state['time_seconds'] = combat_seconds
