import random
import tkinter as tk
from resources import Entity

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BALL_DIAMETER = 30
BALL_RADIUS = BALL_DIAMETER / 2
TOTAL_ENTITIES = 30
FRAME_RATE_MS = 16


SPRITE_PATHS = {
    'rock': 'assets/rock.png',
    'paper': 'assets/paper.png',
    'scissors': 'assets/scissors.png'
}

def update_game(canvas, entities):
    for entity in entities:
        entity.move()

    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            entities[i].check_collision(entities[j])

    canvas.after(FRAME_RATE_MS, update_game, canvas, entities)


def main():
    root = tk.Tk()
    root.title("Rock Paper Scissors Kinetic Battle")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#1e1e2e")
    canvas.pack(fill="both", expand=True)

    Entity.load_sprites(SPRITE_PATHS, BALL_DIAMETER)

    entities = []
    types = ['rock', 'paper', 'scissors']

    for _ in range(TOTAL_ENTITIES):
        x = random.randint(int(BALL_DIAMETER), WINDOW_WIDTH - int(BALL_DIAMETER))
        y = random.randint(int(BALL_DIAMETER), WINDOW_HEIGHT - int(BALL_DIAMETER))

        x_vel = random.choice([-3, -2, 2, 3])
        y_vel = random.choice([-3, -2, 2, 3])

        entity_type = random.choice(types)

        entity = Entity(canvas, x, y, BALL_RADIUS, x_vel, y_vel, entity_type)
        entities.append(entity)

    update_game(canvas, entities)

    root.mainloop()


if __name__ == "__main__":
    main()