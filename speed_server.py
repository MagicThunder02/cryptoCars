import random

import numpy as np
from crypto_params import p, g


class SpeedServer:
    def __init__(self):
        self.terrains = {
            "Sunny": [random.randint(1, p - 1) for _ in range(10)],
            "Rainy": [random.randint(1, p - 1) for _ in range(10)],
            "Snowy": [random.randint(1, p - 1) for _ in range(10)],
        }

        self.current_terrain = "Sunny"
        self.weights = self.terrains["Sunny"]

    def calc_weight_associated_sk(self, master_sk):

        sky = 0
        for i in range(len(self.weights)):
            sky += (self.weights[i] * master_sk[i]) % (p - 1)
        sky = sky % (p - 1)

        return sky

    def calc_weight_associated_cts(self, ct):
        cty = []
        for i in range(len(ct)):
            cty.append(pow(ct[i], self.weights[i], p))
        return cty

    def calc_functional_key(self, master_sk, mask):
        """
        Calculate the functional key sk_y = <weights * mask, master_sk>
        where y = weights * mask (element-wise)
        """
        sky = 0
        for i in range(len(self.weights)):
            y_i = (self.weights[i] * mask[i]) % (p - 1)
            sky += (y_i * master_sk[i]) % (p - 1)
        sky = sky % (p - 1)
        return sky

    def change_terrain(self, new_terrain):
        # cambiando il terreno si cambiano i pesi associati alla funzione speed
        if new_terrain in self.terrains:
            self.weights = self.terrains[new_terrain]
            self.current_terrain = new_terrain
            return True
        return False

    def get_current_terrain(self):
        return self.current_terrain
