""" Class attack """

class Attack:
    def __init__(self, **kwargs):
        self._name = kwargs.get('name')
        self._value = kwargs.get('value')
        self._type = kwargs.get('type')
        self._channeled_time = kwargs.get('channeled_time')
        self._cast_time = kwargs.get('cast_time')
        self._duration = kwargs.get('duration')
        self._buffs = kwargs.get('bufs')
        self._debuffs = kwargs.get('debufs')

    def hit(self, critical=False):
        average_damage = None
        skill_coef_max_magicka = 0.1
        max_magicka = 29500
        skill_coef_spell_damage = 1.05
        spell_damage = 4500
        flat_damage_amp = 0
        skill_level = 0.033

        if skill_coef_spell_damage/skill_coef_max_magicka > 10.6 or skill_coef_spell_damage/skill_coef_max_magicka < 10.4:
            print("Posible error", skill_coef_spell_damage/skill_coef_max_magicka)

        damage = (skill_coef_max_magicka * max_magicka + skill_coef_spell_damage * spell_damage + flat_damage_amp)
        dmg.append(damage + damage*skill_level)

        spell_critical_chance = 0.62
        spell_critical_damage = 0.62
        damage_done = 0
        armor_debuff = 0
        spell_armor_mitigation = 5600
        armor_penetrarion_perc = 0
        damage_taken = 0
        execute_bonus = 0
        bloodthisty_bonus = 0

        dmg.append(1 + spell_critical_chance * spell_critical_damage)
        dmg.append(1 + damage_done)
        dmg.append(1 - ((((18200 - armor_debuff)*(1 - 0)) - spell_armor_mitigation)/(50*1000))) # Proviene de: 100% de la armadura equivale a una resistencia de 50k
        dmg.append(1 + damage_taken)
        dmg.append(1 + execute_bonus)
        dmg.append(1 + bloodthisty_bonus)

        print(dmg)
        average_damage = int(prod(dmg))
        pvp_average_damage = average_damage//2
        print(average_damage, pvp_average_damage)
