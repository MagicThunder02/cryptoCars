import random

import numpy as np
from car import Car
from prover import Prover
from speed_server import SpeedServer
from user import User
from crypto_params import p, g


class GameServer:
    def __init__(self):
        self.users = {}
        self.speedServer = SpeedServer()
        self.mask = [random.randint(1, p - 1) for _ in range(10)]
        self.master_sk = [random.randint(1, p - 1) for _ in range(10)]
        self.master_pk = [pow(g, sk, p) for sk in self.master_sk]

        self.race_participants = []
        self.cars_created_this_race = (
            set()
        )  # Track users who created cars for current race

    def create_user(self, user_id):
        if user_id not in self.users:
            user = User(user_id)
            self.users[user_id] = user
            self.create_car(user_id)
            return user
        return self.users[user_id]

    def create_car(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"

        # Check if user already created a car for this race
        if user_id in self.cars_created_this_race:
            return False, "You can only create one car per race"

        # ottengo i flags dell'auto gia protetti da DLOG
        car = Car(user_id)

        # ciframento delle flags da parte del server
        r = random.randint(1, p - 1)
        ct = pow(g, r, p)
        car.set_ct(ct)
        ciphered_flags = [
            (pow(self.master_pk[i], r, p) * flag) % p
            for i, flag in enumerate(car.get_flags())
        ]

        car.set_flags(ciphered_flags)
        user.add_car(car)

        # Mark that this user has created a car for this race
        self.cars_created_this_race.add(user_id)

        return True, f"Car created (total: {len(user.cars)})"

    def get_user(self, user_id):
        return self.users.get(user_id)

    def calculate_speed(self, car):
        flags = car.get_flags()  # Encrypted flags: ct_i = h_i^r · g^x_i
        ct = car.get_ct()  # ct_0 = g^r

        # Server computes: masked_sk = mask * master_sk (element-wise)
        masked_sk = [(self.mask[i] * self.master_sk[i]) % (p - 1) for i in range(10)]

        # SpeedServer computes: sk_y = <weights, masked_sk> = sum(weights[i] * masked_sk[i])
        sky = self.speedServer.calc_weight_associated_sk(masked_sk)

        # Calculate ct_i^weight_i for each i
        cty = self.speedServer.calc_weight_associated_cts(flags)

        # Apply mask: (ct_i^weight_i)^mask_i = ct_i^(weight_i * mask_i)
        cty_masked = []
        for i in range(len(cty)):
            cty_masked.append(pow(cty[i], self.mask[i], p))

        # Compute numerator: ∏ ct_i^(weight_i * mask_i)
        numerator = 1
        for ct_val in cty_masked:
            numerator = (numerator * ct_val) % p

        # Compute denominator: ct_0^sk_y
        denominator = pow(ct, sky, p)
        denominator_inv = pow(denominator, -1, p)

        # Result: numerator / denominator = g^<x, weights*mask>
        speed = (numerator * denominator_inv) % p
        car.set_speed(speed)
        return speed

    def train_car(self, user_id, car_index, indices_to_train):
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"

        if not user.spend_xpf(1):
            return False, "Insufficient XPF"

        if car_index < 0 or car_index >= len(user.cars):
            return False, "Invalid car index"

        car = user.cars[car_index]
        flags = car.get_flags()
        for idx in indices_to_train:
            if 0 <= idx < 10:
                change = random.randint(-20, 20)
                flags[idx] = (flags[idx] * pow(g, change, p)) % p

        car.set_flags(flags)
        return True, "Training completed"

    def register_for_race(self, user_id, car_index):
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"

        if not user.spend_xpf(1):
            return False, "Insufficient XPF"

        if car_index < 0 or car_index >= len(user.cars):
            return False, "Invalid car index"

        self.race_participants.append((user_id, car_index))
        return True, "Registered for race"

    def run_race(self):
        if not self.race_participants:
            # Reset the car creation tracking even if no participants
            self.cars_created_this_race.clear()
            return None, "No participants"

        results = []
        for user_id, car_index in self.race_participants:
            user = self.users[user_id]
            car = user.cars[car_index]
            speed = self.calculate_speed(car)
            results.append((user_id, car_index, speed))

        results.sort(key=lambda x: x[2], reverse=True)
        winner_id = results[0][0]

        winner = self.users[winner_id]
        winner.add_xpf(100)

        self.race_participants = []

        # Reset the car creation tracking for the next race
        self.cars_created_this_race.clear()

        return results, winner_id

    def change_terrain(self, new_terrain):
        """Change the terrain for the speed calculation"""
        return self.speedServer.change_terrain(new_terrain)

    def get_current_terrain(self):
        """Get the current terrain"""
        return self.speedServer.get_current_terrain()

    def prove_speed(self, user_id, car_index):
        """Verify that encryption/decryption of speed calculation is correct"""
        user = self.users.get(user_id)
        if not user:
            return False, "User not found", None, None

        if car_index < 0 or car_index >= len(user.cars):
            return False, "Invalid car index", None, None

        car = user.cars[car_index]

        # Calculate speed using encrypted flags (homomorphic calculation)
        encrypted_speed = self.calculate_speed(car)

        # Calculate speed using prover (with secret flags)
        prover = Prover()
        proven_speed = prover.prove_speed(car, self.mask, self.speedServer.weights)

        # Compare the two speeds
        is_equal = encrypted_speed == proven_speed

        return True, "Speeds compared", encrypted_speed, proven_speed, is_equal
