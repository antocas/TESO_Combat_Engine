""" Main for testing """
import random
from src.MC import dummy
from src.MC import attack
from src.MC import combat_queue

from src.Instances.model_attack import *

import streamlit as st

def main_combat_test():
    initial_health = 300000
    # initial_health = 21000000

    test_dummy = dummy.Dummy(health=initial_health)
    queue = combat_queue.QueueAttack()
    seconds = 0


    circular = [wall_of_elements, mystic_orb, barbed_trap]
    test_dummy.set_debuff(minor_breach)

    while test_dummy.attributes["health_bar"] > 0:
        queue.add_attack(light_attack)
        for to_renovate in circular:
            if not queue.in_queue(to_renovate._name):
                queue.add_attack(to_renovate)
                break
        
        # DAMAGE = 5000
        CRIT_PROB = 0.91
        MAX_CRIT = 0.91
        PENETRATION = 5395
        # PENETRATION = 18200

        test_dummy.apply_debuffs()
        
        # RONDA DE ATAQUES
        for name, attack in queue._attacks.items():
            DAMAGE = attack._value
            if random.random() <= CRIT_PROB:
                DAMAGE += DAMAGE*MAX_CRIT
            test_dummy.hit_dummy(DAMAGE, PENETRATION)
            # TEST
            queue.delete_attack_from_queue(attack._name)
        
        test_dummy.reset_resistances()
        seconds += 1

    combat_minutes = seconds//60
    combat_seconds = seconds%60
    print(f"Derrotado en {combat_minutes} minutos, {combat_seconds} segundos, con dps {initial_health//seconds}")
    st.session_state['dps'] = initial_health//seconds
    st.session_state['time'] = seconds