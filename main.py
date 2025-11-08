import tkinter as tk
from tkinter import ttk, messagebox
from principal_server import GameServer


class GameGUI:
    def __init__(self):
        self.server = GameServer()
        self.setup_users()

        self.root = tk.Tk()
        self.root.title("Crypto Cars Game")

        self.create_widgets()
        self.update_display()

        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        self.root.geometry(f"{max(width, 1000)}x{max(height, 600)}")
        self.root.minsize(900, 600)

    def setup_users(self):
        for name in ["Alice", "Bob", "Charlie"]:
            self.server.create_user(name)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="CRYPTO CARS GAME", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=3, pady=10
        )

        left_frame = ttk.LabelFrame(main_frame, text="Users Stats", padding="10")
        left_frame.grid(row=1, column=0, padx=5, sticky=(tk.N, tk.S, tk.W, tk.E))

        scrollbar_users_y = ttk.Scrollbar(left_frame, orient=tk.VERTICAL)
        scrollbar_users_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_users_x = ttk.Scrollbar(left_frame, orient=tk.HORIZONTAL)
        scrollbar_users_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.users_text = tk.Text(
            left_frame,
            height=15,
            wrap=tk.NONE,
            xscrollcommand=scrollbar_users_x.set,
            yscrollcommand=scrollbar_users_y.set,
        )
        self.users_text.pack(fill=tk.BOTH, expand=True)
        scrollbar_users_x.config(command=self.users_text.xview)
        scrollbar_users_y.config(command=self.users_text.yview)

        middle_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        middle_frame.grid(row=1, column=1, padx=5, sticky=(tk.N, tk.W, tk.E))

        ttk.Label(middle_frame, text="Select User:").grid(
            row=0, column=0, pady=5, sticky=tk.W
        )
        self.user_var = tk.StringVar(value="Alice")
        user_combo = ttk.Combobox(
            middle_frame,
            textvariable=self.user_var,
            values=["Alice", "Bob", "Charlie"],
            state="readonly",
        )
        user_combo.grid(row=0, column=1, pady=5)
        user_combo.bind("<<ComboboxSelected>>", lambda e: self.on_user_changed())

        ttk.Label(middle_frame, text="Select Car:").grid(
            row=1, column=0, pady=5, sticky=tk.W
        )
        self.car_var = tk.StringVar(value="0")
        self.car_combo = ttk.Combobox(
            middle_frame, textvariable=self.car_var, state="readonly"
        )
        self.car_combo.grid(row=1, column=1, pady=5)

        ttk.Label(middle_frame, text="Train Indices:").grid(
            row=2, column=0, pady=5, sticky=tk.W
        )

        checkboxes_frame = ttk.Frame(middle_frame)
        checkboxes_frame.grid(row=2, column=1, pady=5, sticky=tk.W)

        self.flag_vars = []
        for i in range(10):
            var = tk.BooleanVar(value=True)
            self.flag_vars.append(var)
            cb = ttk.Checkbutton(checkboxes_frame, text=str(i), variable=var)
            cb.grid(row=0, column=i, padx=2)

        ttk.Button(middle_frame, text="Train Car", command=self.train_car).grid(
            row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E)
        )
        ttk.Button(middle_frame, text="Create New Car", command=self.create_car).grid(
            row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E)
        )

        ttk.Separator(middle_frame, orient=tk.HORIZONTAL).grid(
            row=5, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E)
        )

        ttk.Label(middle_frame, text="Terrain:").grid(
            row=6, column=0, pady=5, sticky=tk.W
        )
        self.terrain_var = tk.StringVar(value="Sunny")
        terrain_combo = ttk.Combobox(
            middle_frame,
            textvariable=self.terrain_var,
            values=["Sunny", "Rainy", "Snowy"],
            state="readonly",
        )
        terrain_combo.grid(row=6, column=1, pady=5)
        terrain_combo.bind("<<ComboboxSelected>>", lambda e: self.change_terrain())

        ttk.Button(middle_frame, text="Prove Speed", command=self.prove_speed).grid(
            row=7, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E)
        )

        ttk.Separator(middle_frame, orient=tk.HORIZONTAL).grid(
            row=8, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E)
        )

        ttk.Label(middle_frame, text="Race Registration:").grid(
            row=9, column=0, columnspan=2, pady=5
        )
        ttk.Button(
            middle_frame, text="Register for Race", command=self.register_race
        ).grid(row=10, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(
            middle_frame, text="RUN RACE", command=self.run_race, style="Accent.TButton"
        ).grid(row=11, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        right_frame = ttk.LabelFrame(main_frame, text="Cars Details", padding="10")
        right_frame.grid(row=1, column=2, padx=5, sticky=(tk.N, tk.S, tk.W, tk.E))

        scrollbar_cars_y = ttk.Scrollbar(right_frame, orient=tk.VERTICAL)
        scrollbar_cars_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_cars_x = ttk.Scrollbar(right_frame, orient=tk.HORIZONTAL)
        scrollbar_cars_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.cars_text = tk.Text(
            right_frame,
            height=15,
            wrap=tk.NONE,
            xscrollcommand=scrollbar_cars_x.set,
            yscrollcommand=scrollbar_cars_y.set,
        )
        self.cars_text.pack(fill=tk.BOTH, expand=True)
        scrollbar_cars_x.config(command=self.cars_text.xview)
        scrollbar_cars_y.config(command=self.cars_text.yview)

        race_frame = ttk.LabelFrame(main_frame, text="Race Info", padding="10")
        race_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        scrollbar_race_y = ttk.Scrollbar(race_frame, orient=tk.VERTICAL)
        scrollbar_race_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_race_x = ttk.Scrollbar(race_frame, orient=tk.HORIZONTAL)
        scrollbar_race_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.race_text = tk.Text(
            race_frame,
            height=8,
            wrap=tk.NONE,
            xscrollcommand=scrollbar_race_x.set,
            yscrollcommand=scrollbar_race_y.set,
        )
        self.race_text.pack(fill=tk.BOTH, expand=True)
        scrollbar_race_x.config(command=self.race_text.xview)
        scrollbar_race_y.config(command=self.race_text.yview)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)

        self.update_car_combo()

    def update_car_combo(self):
        user_id = self.user_var.get()
        user = self.server.get_user(user_id)
        if user:
            car_count = len(user.cars)
            self.car_combo["values"] = [str(i) for i in range(car_count)]
            if car_count > 0:
                self.car_var.set("0")

    def on_user_changed(self):
        self.update_display()

    def update_display(self):
        self.users_text.delete(1.0, tk.END)

        # Show current terrain
        current_terrain = self.server.get_current_terrain()
        self.users_text.insert(tk.END, f"Current Terrain: {current_terrain}\n")
        self.users_text.insert(tk.END, "=" * 30 + "\n\n")

        for user_id in ["Alice", "Bob", "Charlie"]:
            user = self.server.get_user(user_id)
            self.users_text.insert(tk.END, f"{user_id}\n")
            self.users_text.insert(tk.END, f"  XPF: {user.xpf}\n")
            self.users_text.insert(tk.END, f"  Cars: {len(user.cars)}\n")
            self.users_text.insert(tk.END, "\n")

        self.cars_text.delete(1.0, tk.END)
        user_id = self.user_var.get()
        user = self.server.get_user(user_id)
        if user:
            self.cars_text.insert(tk.END, f"{user_id}'s Cars:\n\n")
            for i, car in enumerate(user.cars):
                speed = self.server.calculate_speed(car)
                self.cars_text.insert(tk.END, f"Car {i}:\n")
                self.cars_text.insert(tk.END, f"  Speed: {speed}\n")
                self.cars_text.insert(tk.END, f"  Flags: {car.flags}\n\n")

        self.update_car_combo()

    def train_car(self):
        user_id = self.user_var.get()
        car_index = int(self.car_var.get())

        indices = [i for i in range(10) if self.flag_vars[i].get()]

        if not indices:
            messagebox.showerror("Error", "Select at least one flag to train")
            return

        user = self.server.get_user(user_id)
        if user.xpf < 1:
            messagebox.showerror("Error", "Insufficient XPF (need 1 XPF)")
            return

        success, msg = self.server.train_car(user_id, car_index, indices)
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

        self.update_display()

    def create_car(self):
        user_id = self.user_var.get()
        success, msg = self.server.create_car(user_id)

        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

        self.update_display()

    def register_race(self):
        user_id = self.user_var.get()
        car_index = int(self.car_var.get())

        success, msg = self.server.register_for_race(user_id, car_index)
        if success:
            self.race_text.insert(
                tk.END, f"{user_id} registered with car {car_index}\n"
            )
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

        self.update_display()

    def run_race(self):
        results, winner = self.server.run_race()

        if results is None:
            messagebox.showwarning("Warning", winner)
            return

        self.race_text.delete(1.0, tk.END)
        self.race_text.insert(tk.END, "=== RACE RESULTS ===\n\n")

        for i, (user_id, car_index, speed) in enumerate(results, 1):
            self.race_text.insert(
                tk.END, f"{i}. {user_id} (car {car_index}): {speed}\n"
            )

        self.race_text.insert(tk.END, f"\n🏆 WINNER: {winner} (+100 XPF)\n")

        messagebox.showinfo("Race Complete", f"Winner: {winner}!")
        self.update_display()

    def change_terrain(self):
        new_terrain = self.terrain_var.get()
        success = self.server.change_terrain(new_terrain)

        if success:
            messagebox.showinfo("Terrain Changed", f"Terrain changed to {new_terrain}!")
            self.update_display()
        else:
            messagebox.showerror("Error", "Failed to change terrain")

    def prove_speed(self):
        user_id = self.user_var.get()
        try:
            car_index = int(self.car_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please select a car")
            return

        success, msg, encrypted_speed, proven_speed, is_equal = self.server.prove_speed(
            user_id, car_index
        )

        if success:
            result_msg = f"Speed Verification for {user_id}'s Car {car_index}\n"
            result_msg += "=" * 50 + "\n\n"
            result_msg += (
                f"🔒 Encrypted Speed (from homomorphic calc): {encrypted_speed}\n\n"
            )
            result_msg += (
                f"🔓 Proven Speed (from secret flags):        {proven_speed}\n\n"
            )
            result_msg += "=" * 50 + "\n"

            if is_equal:
                result_msg += "\n✓ MATCH! The values are equal!\n"
                result_msg += "Encryption/Decryption working correctly!"
                messagebox.showinfo("Speed Proof Verification", result_msg)
            else:
                result_msg += "\n✗ NO MATCH! The values are different!\n"
                result_msg += "Check your encryption/decryption implementation!"
                messagebox.showwarning("Speed Proof Verification", result_msg)
        else:
            messagebox.showerror("Error", msg)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GameGUI()
    app.run()
