from server import GameServer


def main():
    server = GameServer()

    print("=== CRYPTO CARS GAME ===\n")

    user1 = server.create_user("Alice")
    user2 = server.create_user("Bob")
    user3 = server.create_user("Charlie")

    print(f"Users created:")
    print(f"  {user1}")
    print(f"  {user2}")
    print(f"  {user3}\n")

    print(f"Alice's car 0: {user1.cars[0]}")
    speed = server.calculate_speed(user1.cars[0])
    print(f"Alice's car 0 speed: {speed}\n")

    print("Alice creates a second car...")
    server.create_car("Alice")
    print(f"  {user1}")
    print(f"  Car 0: {user1.cars[0]}")
    print(f"  Car 1: {user1.cars[1]}\n")

    print("Alice trains car 1 (indices 0, 3, 7)...")
    success, msg = server.train_car("Alice", 1, [0, 3, 7])
    print(f"  {msg}")
    print(f"  {user1}")
    print(f"  Car 1: {user1.cars[1]}")
    print(f"  Car 1 speed: {server.calculate_speed(user1.cars[1])}\n")

    print("Bob trains his car 0 (all indices)...")
    server.train_car("Bob", 0, list(range(10)))
    print(f"  {user2}")
    print(f"  Bob's car 0 speed: {server.calculate_speed(user2.cars[0])}\n")

    print("Registering for race...")
    server.register_for_race("Alice", 1)
    server.register_for_race("Bob", 0)
    server.register_for_race("Charlie", 0)

    print(f"  Alice: {user1}")
    print(f"  Bob: {user2}")
    print(f"  Charlie: {user3}\n")

    print("Running race...")
    results, winner = server.run_race()
    print(f"\nRace Results:")
    for i, (user_id, car_index, speed) in enumerate(results, 1):
        print(f"  {i}. {user_id} (car {car_index}): {speed}")
    print(f"\nWinner: {winner}!")

    print(f"\nFinal balances:")
    for user_id in ["Alice", "Bob", "Charlie"]:
        user = server.get_user(user_id)
        print(f"  {user}")


if __name__ == "__main__":
    main()
