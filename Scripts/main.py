import cv2
import numpy as np

from matplotlib import pyplot as plt

# TODO - Change fake violet-pip.jpg to real image template.
# - Collect screenshots with violet-pip visible

class Grid:
    def __init__(self, _tiles):

        # Set row of tiles ('normalise' y by subtracting minimum.)
        min_y = min([t.iy for t in _tiles])
        for t in _tiles:
            t.row = int(round((t.iy - min_y) / 100))
            t.set_index()

        tiles.sort(key=lambda x: x.index)
        self.tiles = [None] * 70
        for t in _tiles:
            self.tiles[t.index] = t

    def get_row(self, num):
        return self.tiles[num * 7:num * 7 + 7]

    def get_column(self, num):
        return self.tiles[num::7]

    def draw(self):
        for t in tiles:
            if t:
                t.draw()

    def __repr__(self):
        out = "#|--0-|--1-|--2-|--3-|--4-|--5-|--6-"
        for r in range(10):
            out += "\n" + str(r) + "|" + "|".join(map(str, self.get_row(r)))
        return out


class Tile:
    def __init__(self, _ix, _iy, _colour, _pip=False):
        self.ix = _ix
        self.iy = _iy
        self.colour = _colour
        self.row = None
        self.col = int(round(_ix / 100))
        self.index = None
        self.pip = _pip

    def set_index(self):
        self.index = self.row * 7 + self.col

    def draw(self):
        colours = {'red': (0, 0, 255), 'green': (0, 255, 0), 'orange': (0, 172, 255), 'pink': (172, 0, 255),
                   'violet': (255, 0, 172)}
        x, y = self.ix, self.iy
        if self.pip:
            w, h = 66, 66
            cv2.circle(img_rgb, (int(x + w / 2), int(y + h / 2)), int(min(w, h) / 2), colours[self.colour], -1)
            cv2.putText(img_rgb, str(self.index), (x + 14, y + 42), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
        else:
            w, h = 92, 65
            cv2.rectangle(img_rgb, (x, y), (x + w, y + h), colours[self.colour], -1)
            cv2.putText(img_rgb, str(self.index), (x + 25, y + 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 255))

    def __str__(self):
        return f"_{self.colour[:3]}"

    def __repr__(self):
        return str(self)


screenshot_num = 12

# Load image, select region, convert to grayscale.
full_img_rgb = cv2.imread('..\Images\Screenshots\Screenshot ' + str(screenshot_num) + ".jpg")
img_rgb = full_img_rgb[180:180 + 890, 580:580 + 690]
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

tiles = []
# BGR
colours = {'red': (0, 0, 255), 'green': (0, 255, 0), 'orange': (0, 172, 255), 'pink': (172, 0, 255),
           'violet': (255, 0, 172)}
for col in colours:
    for pip in [True, False]:
        if pip:
            template = cv2.imread(f"../Images/Templates/{col}-pip.jpg", 0)
        else:
            template = cv2.imread(f"../Images/Templates/{col}.jpg", 0)

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.92
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            # Over-matching fix: Only add/draw tiles that are far enough away from already found tiles.
            for t in tiles:
                dx = abs(pt[0] - t.ix)
                dy = abs(pt[1] - t.iy)
                if dx < 10 and dy < 10:
                    break
            else:  # I'm so happy that I used this! :)
                tiles.append(Tile(_ix=pt[0], _iy=pt[1], _colour=col, _pip=pip))


griddy = Grid(tiles)
griddy.draw()

print(griddy)

cv2.imshow('res.png', img_rgb)
cv2.waitKey()
cv2.destroyAllWindows()

print("done")

DROP = -1
PICK = 0
SWITCH = 1
LEFT = 2
RIGHT = 3
moves = [[PICK], [SWITCH, PICK], [PICK, SWITCH, DROP, SWITCH, PICK]]



