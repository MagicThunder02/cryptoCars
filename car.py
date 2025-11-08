import random
from generator_server import Oracle


class Car:
    def __init__(self, owner_id):
        self.oracle = Oracle()
        self.owner_id = owner_id
        self.speed = 0

        # Generate flags and store both encrypted and secret values
        flag_data = [self.oracle.generate_flag() for _ in range(10)]
        self.flags = [flag for flag, _ in flag_data]
        self.secretFlags = [secret for _, secret in flag_data]

        self.ct = None

    def set_speed(self, speed):
        self.speed = speed

    def get_flags(self):
        return self.flags.copy()

    def set_flags(self, new_flags):
        self.flags = new_flags

    def set_ct(self, ct):
        self.ct = ct

    def get_ct(self):
        return self.ct

    def __repr__(self):
        return f"Car(owner={self.owner_id}, flags={self.flags})"
