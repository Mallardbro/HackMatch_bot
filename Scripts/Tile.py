import cv2


class Tile:
    def __init__(self, _ix, _iy, _colour, _pip=False):
        self.ix = _ix
        self.iy = _iy
        self.colour = _colour
        self.row = None
        self.col = int(round(_ix / 100))
        self.index = None
        self.text = None
        self.pip = _pip
        self.accessible = 99
        self.neighbours = {"left": None, "right": None, "up": None, "down": None}
        self.chained = -1

    def set_index(self):
        self.index = self.row * 7 + self.col
        self.text = str(self.index)

    def draw(self, _image):
        colours = {'red': (0, 0, 255), 'green': (0, 255, 0), 'orange': (0, 172, 255), 'pink': (172, 0, 255),
                   'violet': (255, 0, 172)}
        x, y = self.ix, self.iy
        if self.pip:
            w, h = 66, 66
            cv2.circle(_image, (int(x + w / 2), int(y + h / 2)), int(min(w, h) / 2), colours[self.colour], -1)
            cv2.putText(_image, self.text, (x + 14, y + 42), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255))
        else:
            w, h = 92, 65
            cv2.rectangle(_image, (x, y), (x + w, y + h), colours[self.colour], -1)
            cv2.putText(_image, self.text, (x + 10, y + 40), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (255, 255, 255))

    def __str__(self):
        return f"_{self.colour[:3]}"

    def __repr__(self):
        return str(self)
