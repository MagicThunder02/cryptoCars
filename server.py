import random
from car import Car
from user import User


class GameServer:
    def __init__(self):
        self.users = {}
        self.race_participants = []

    def create_user(self, user_id):
        if user_id not in self.users:
            user = User(user_id)
            car = Car(user_id)
            user.add_car(car)
            self.users[user_id] = user
            return user
        return self.users[user_id]

    def create_car(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"

        car = Car(user_id)
        user.add_car(car)
        return True, f"Car created (total: {len(user.cars)})"

    def get_user(self, user_id):
        return self.users.get(user_id)

    def calculate_speed(self, car):
        return sum(car.flags)

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
                flags[idx] += change

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
