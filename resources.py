import math
from PIL import Image, ImageTk

class Entity:
    SPRITES = {}

    @classmethod
    def load_sprites(cls, sprite_paths, diameter):
        #Call this once before creating entities to load image assets.
        size = int(diameter)
        for entity_type, path in sprite_paths.items():
            img = Image.open(path).resize((size, size))
            cls.SPRITES[entity_type] = ImageTk.PhotoImage(img)

    def __init__(self, canvas, x, y, radius, xVelocity, yVelocity, entity_type):
        self.canvas = canvas
        self.radius = radius
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.type = entity_type

        self.image = canvas.create_image(
            x, y, image=Entity.SPRITES[self.type]
        )

    def set_type(self, new_type):
        #Swaps the entity type and updates its canvas texture
        if self.type != new_type:
            self.type = new_type
            self.canvas.itemconfig(self.image, image=Entity.SPRITES[self.type])

    def get_center(self):
        coords = self.canvas.coords(self.image)
        return coords[0], coords[1]

    def move(self):
        x, y = self.get_center()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if x + self.radius >= width or x - self.radius <= 0:
            self.xVelocity = -self.xVelocity
        if y + self.radius >= height or y - self.radius <= 0:
            self.yVelocity = -self.yVelocity

        self.canvas.move(self.image, self.xVelocity, self.yVelocity)

    def check_collision(self, other):
        x1, y1 = self.get_center()
        x2, y2 = other.get_center()

        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        min_distance = self.radius + other.radius

        if 0 < distance < min_distance:
            self.xVelocity, other.xVelocity = other.xVelocity, self.xVelocity
            self.yVelocity, other.yVelocity = other.yVelocity, self.yVelocity

            overlap = 0.5 * (min_distance - distance)
            nx, ny = dx / distance, dy / distance
            self.canvas.move(self.image, -nx * overlap, -ny * overlap)
            self.canvas.move(other.image, nx * overlap, ny * overlap)


            self.resolve_rps_outcome(other)

    def resolve_rps_outcome(self, other):
        beats = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }

        if beats[self.type] == other.type:
            other.set_type(self.type)
        elif beats[other.type] == self.type:
            self.set_type(other.type)