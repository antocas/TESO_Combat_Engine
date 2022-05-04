""" Class attack """

from src.MC.character import Character


class Attack:
    def __init__(self, attack_data_log):
        self.attributes = attack_data_log

    def calculate_damage(self, character:Character):
        pass
