class Shape:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, draw_obj):
        raise NotImplementedError("Subclasses must implement draw()")

class Circle(Shape):
    def draw(self, draw_obj):
        draw_obj.ellipse([
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        ], fill=self.color)

class Square(Shape):
    def draw(self, draw_obj):
        draw_obj.rectangle([
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        ], fill=self.color)

class Triangle(Shape):
    def draw(self, draw_obj):
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]
        draw_obj.polygon(points, fill=self.color)
