import random


class Car:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.flags = [random.randint(0, 1000) for _ in range(10)]

    def get_flags(self):
        return self.flags.copy()

    def set_flags(self, new_flags):
        self.flags = [max(0, min(1000, flag)) for flag in new_flags]

    def __repr__(self):
        return f"Car(owner={self.owner_id}, flags={self.flags})"
