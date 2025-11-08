import random
from crypto_params import p, g

import secrets


class Oracle:
    def __init__(self):
        pass

    def generate_flag(self):
        x = random.randint(1, 999)
        return pow(g, x, p), x
