import random
import tkinter as tk
from resources import Entity


class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Kinetic Battle")
        self.root.geometry("450x580")
        self.root.resizable(False, False)

        self.menu_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.menu_frame.pack(fill="both", expand=True)

        self.game_frame = tk.Frame(self.root, bg="#11111b")

        self.canvas = None
        self.entities = []
        self.is_running = False
        self.is_paused = False
        self.loop_job = None

        self.build_menu()

    def build_menu(self):
        title = tk.Label(
            self.menu_frame, text="RPS Kinetic Battle",
            font=("Helvetica", 20, "bold"), fg="#cdd6f4", bg="#1e1e2e"
        )
        title.pack(pady=20)

        self.rock_entry = self.create_entry("Initial Rocks:", "10")
        self.paper_entry = self.create_entry("Initial Papers:", "10")
        self.scissors_entry = self.create_entry("Initial Scissors:", "10")
        self.speed_entry = self.create_entry("Entity Speed (1-10):", "3")

        btn_frame = tk.Frame(self.menu_frame, bg="#1e1e2e")
        btn_frame.pack(pady=25)

        start_btn = tk.Button(
            btn_frame, text="Start Simulation", font=("Helvetica", 12, "bold"),
            bg="#a6e3a1", fg="#11111b", width=14, command=self.start_game
        )
        start_btn.pack(side="left", padx=5)

        quit_btn = tk.Button(
            btn_frame, text="Quit", font=("Helvetica", 12, "bold"),
            bg="#f38ba8", fg="#11111b", width=10, command=self.root.destroy
        )
        quit_btn.pack(side="left", padx=5)

    def create_entry(self, label_text, default_val):
        frame = tk.Frame(self.menu_frame, bg="#1e1e2e")
        frame.pack(fill="x", padx=60, pady=8)

        lbl = tk.Label(frame, text=label_text, fg="#cdd6f4", bg="#1e1e2e", font=("Helvetica", 11))
        lbl.pack(side="left")

        entry = tk.Entry(
            frame, font=("Helvetica", 11), width=6, bg="#313244",
            fg="#cdd6f4", insertbackground="#cdd6f4", justify="center"
        )
        entry.insert(0, default_val)
        entry.pack(side="right")
        return entry

    def get_input_val(self, entry_widget, fallback_val):
        try:
            val = int(entry_widget.get().strip())
            return max(1, val)
        except ValueError:
            return fallback_val

    def build_game_ui(self):
        self.control_bar = tk.Frame(self.game_frame, bg="#181825", height=50)
        self.control_bar.pack(fill="x", side="top", padx=10, pady=5)

        self.pause_btn = tk.Button(
            self.control_bar, text="Pause", font=("Helvetica", 10, "bold"),
            bg="#f9e2af", fg="#11111b", command=self.toggle_pause
        )
        self.pause_btn.pack(side="left", padx=5, pady=5)

        restart_btn = tk.Button(
            self.control_bar, text="Restart", font=("Helvetica", 10, "bold"),
            bg="#89b4fa", fg="#11111b", command=self.restart_game
        )
        restart_btn.pack(side="left", padx=5, pady=5)

        menu_btn = tk.Button(
            self.control_bar, text="Menu", font=("Helvetica", 10, "bold"),
            bg="#f38ba8", fg="#11111b", command=self.return_to_menu
        )
        menu_btn.pack(side="left", padx=5, pady=5)

        self.score_label = tk.Label(
            self.control_bar, text="Rock: 0 | Paper: 0 | Scissors: 0",
            font=("Helvetica", 11, "bold"), fg="#cdd6f4", bg="#181825"
        )
        self.score_label.pack(side="right", padx=15)

        self.canvas = tk.Canvas(self.game_frame, width=800, height=550, bg="#1e1e2e")
        self.canvas.pack(fill="both", expand=True)

    def start_game(self):
        self.menu_frame.pack_forget()

        self.root.geometry("800x620")
        self.game_frame.pack(fill="both", expand=True)

        if not self.canvas:
            self.build_game_ui()

        self.spawn_entities()
        self.is_running = True
        self.is_paused = False
        self.pause_btn.config(text="Pause")
        self.game_loop()

    def spawn_entities(self):
        self.canvas.delete("all")
        self.entities.clear()

        n_rocks = self.get_input_val(self.rock_entry, fallback_val=10)
        n_papers = self.get_input_val(self.paper_entry, fallback_val=10)
        n_scissors = self.get_input_val(self.scissors_entry, fallback_val=10)
        speed = self.get_input_val(self.speed_entry, fallback_val=3)

        BALL_DIAMETER = 30
        BALL_RADIUS = BALL_DIAMETER / 2
        width, height = 800, 550

        Entity.load_sprites({
            'rock': 'assets/rock.png',
            'paper': 'assets/paper.png',
            'scissors': 'assets/scissors.png'
        }, BALL_DIAMETER)

        spawn_data = [('rock', n_rocks), ('paper', n_papers), ('scissors', n_scissors)]
        for e_type, count in spawn_data:
            for _ in range(count):
                x = random.randint(int(BALL_DIAMETER), width - int(BALL_DIAMETER))
                y = random.randint(int(BALL_DIAMETER), height - int(BALL_DIAMETER))
                vx = random.choice([-1, 1]) * speed
                vy = random.choice([-1, 1]) * speed
                self.entities.append(Entity(self.canvas, x, y, BALL_RADIUS, vx, vy, e_type))

    def update_scoreboard(self):
        counts = {'rock': 0, 'paper': 0, 'scissors': 0}
        for entity in self.entities:
            counts[entity.type] += 1

        self.score_label.config(
            text=f"🎱 Rock: {counts['rock']} | 📄 Paper: {counts['paper']} | ✂️Scissors: {counts['scissors']}"
        )
        return counts

    def check_win_condition(self, counts):
        active_types = [e_type for e_type, count in counts.items() if count > 0]

        if len(active_types) == 1:
            winner = active_types[0].upper()
            self.is_running = False


            self.canvas.create_rectangle(200, 200, 600, 350, fill="#11111b", outline="#a6e3a1", width=3)
            self.canvas.create_text(
                400, 250, text=f"🎉 {winner} WINS! 🎉",
                font=("Helvetica", 24, "bold"), fill="#a6e3a1"
            )
            self.canvas.create_text(
                400, 300, text="Click Restart or Menu to play again",
                font=("Helvetica", 12), fill="#cdd6f4"
            )

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_btn.config(text="Resume")
        else:
            self.pause_btn.config(text="Pause")
            self.game_loop()

    def restart_game(self):
        if self.loop_job:
            self.root.after_cancel(self.loop_job)
        self.spawn_entities()
        self.is_running = True
        self.is_paused = False
        self.pause_btn.config(text="Pause")
        self.game_loop()

    def return_to_menu(self):
        self.is_running = False
        if self.loop_job:
            self.root.after_cancel(self.loop_job)

        self.game_frame.pack_forget()
        self.root.geometry("450x580")
        self.menu_frame.pack(fill="both", expand=True)

    def game_loop(self):
        if not self.is_running or self.is_paused:
            return

        for entity in self.entities:
            entity.move()

        for i in range(len(self.entities)):
            for j in range(i + 1, len(self.entities)):
                self.entities[i].check_collision(self.entities[j])


        counts = self.update_scoreboard()
        self.check_win_condition(counts)

        if self.is_running:
            self.loop_job = self.root.after(16, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()