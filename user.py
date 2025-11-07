class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.xpf = 10
        self.cars = []

    def add_xpf(self, amount):
        self.xpf += amount

    def spend_xpf(self, amount):
        if self.xpf >= amount:
            self.xpf -= amount
            return True
        return False

    def add_car(self, car):
        self.cars.append(car)

    def __repr__(self):
        return f"User(id={self.user_id}, XPF={self.xpf}, cars={len(self.cars)})"
