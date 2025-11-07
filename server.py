import random

import numpy as np
from car import Car
from server_speed import SpeedServer
from user import User
from crypto_params import p, g


class GameServer:
    def __init__(self):
        self.users = {}
        self.speedServer = SpeedServer()
        self.master_sk = [random.randint(1, p - 1) for _ in range(10)]
        self.master_pk = [pow(g, sk, p) for sk in self.master_sk]

        self.race_participants = []

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
        return True, f"Car created (total: {len(user.cars)})"

    def get_user(self, user_id):
        return self.users.get(user_id)

    def calculate_speed(self, car):
        flags = car.get_flags()
        ct = car.get_ct()
        sky = int(self.speedServer.calc_weight_associated_sk(self.master_sk))
        cty = self.speedServer.calc_weight_associated_cts(flags)
        ct_sky = pow(ct, sky, p)
        ct_sky_inv = pow(ct_sky, -1, p)
        speed = (np.prod(cty) * ct_sky_inv) % p
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

        return results, winner_id
