import random

import numpy as np
from crypto_params import p, g


class SpeedServer:
    def __init__(self):
        terrains = {
            "Sunny": [random.randint(1, p - 1) for _ in range(10)],
            "Rainy": [random.randint(1, p - 1) for _ in range(10)],
            "Snowy": [random.randint(1, p - 1) for _ in range(10)],
        }

        self.weights = terrains["Sunny"]

    def calc_weight_associated_sk(self, master_sk):
        sky = np.dot(self.weights, master_sk) % (p - 1)
        return sky

    def calc_weight_associated_cts(self, ct):
        cty = []
        for i in range(len(ct)):
            cty.append(pow(ct[i], self.weights[i], p))
        return cty

    def change_terrain(self, new_terrain):
        # cambiando il terreno si cambiano i pesi associati alla funzione speed
        self.weights = self.terrains[new_terrain]
