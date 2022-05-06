""" Class character """

class Character:
    def __init__(self, atributes):
        self.attributes = atributes

    def __str__(self):
        return str(self.attributes)

    def as_dict(self):
        return self.attributes

    def apply_buffs():
        pass

    def next_attack(self):
        pass

    @property
    def name(self):
        return self.attributes.get("name") or ""
    @property
    def max_magicka(self):
        return self.attributes.get("max_magicka") or 0
    @property
    def class_name(self):
        return self.attributes.get("class") or ""
    @property
    def spell_damage(self):
        return self.attributes.get("spell_damage") or 0
    @property
    def spell_critical(self):
        return self.attributes.get("spell_critical") or 0
    @property
    def spell_penetration(self):
        return self.attributes.get("spell_penetration") or 0
    @property
    def main_bar(self):
        return self.attributes.get("main_bar") or ""
    @property
    def second_bar(self):
        return self.attributes.get("second_bar") or ""
