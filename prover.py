import numpy as np
from crypto_params import g, p


class Prover:
    def __init__(self):
        pass

    def prove_speed(self, car, mask, weights):
        """
        Calculate speed using secret flags directly

        Args:
            car: Car object with secretFlags
            mask: mask array from server
            weights: weights array from speed server
        """
        flags = car.secretFlags

        # Compute y = weights · mask (element-wise), keeping in modular arithmetic
        y = [(weights[i] * mask[i]) % (p - 1) for i in range(len(weights))]
        
        # Compute scalar = <x, y> = sum(x[i] * y[i]) mod (p-1)
        scalar_p = sum(flags[i] * y[i] for i in range(len(flags))) % (p - 1)
        speed = pow(g, scalar_p, p)
        return speed
