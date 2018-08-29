import cv2
import numpy as np
from matplotlib import pyplot as plt


class Grid:
    def __init__(self):
        self.tiles = []

    def get_row(self, num):
        return [t for t in self.tiles if t.row == num]

    def get_column(self,num):
        return [t for t in self.tiles if t.col == num]

    def __repr__(self):
        # Flawed due to empty tiles. Rehaul needed.
        out = ""
        indexes = [_t.index for _t in self.tiles]
        for i in range(70):
            if i in indexes:
                out += "|" + self.tiles[i].colour[:2]
            else:
                out += "|--"
            if i%7 == 6:
                out += "\n"
        return out


class Tile:
    def __init__(self, _ix, _iy, _colour):
        self.ix = _ix
        self.iy = _iy
        self.colour = _colour
        self.row = None
        self.col = int(round(_ix / 100))
        self.index = None

    def set_index(self):
        self.index = self.row * 7 + self.col


tiles = []

screenshot_num = 12

full_img_rgb = cv2.imread('..\Images\Screenshots\Screenshot ' + str(screenshot_num) + ".jpg")

img_rgb = full_img_rgb[180:180 + 890, 580:580 + 690]
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# BGR
colours = {'red': (0, 0, 255), 'green': (0, 255, 0), 'orange': (0, 172, 255), 'pink': (172, 0, 255),
           'purple': (255, 0, 172)}
for col in colours:
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
            tiles.append(Tile(_ix=pt[0], _iy=pt[1], _colour=col))
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), colours[col], -1)
            # cv2.circle(img_rgb, (pt[0],pt[1]), 10, (255, 255, 255))

griddy = Grid()

# Set row of tiles ('normalise' y by subtracting minimum.)
min_y = min([t.iy for t in tiles])
for t in tiles:
    t.row = int(round((t.iy - min_y) / 100))
    t.set_index()
    cv2.putText(img_rgb, (" " + str(t.index))[1:], (t.ix + 25, t.iy + 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))

tiles.sort(key=lambda x: x.index)
DROP = -1
PICK = 0
SWITCH = 1
LEFT = 2
RIGHT = 3
moves = [[PICK], [SWITCH, PICK], [PICK, SWITCH, DROP, SWITCH, PICK]]

griddy.tiles = tiles
print(griddy)

cv2.imshow('res.png', img_rgb)
cv2.waitKey()
cv2.destroyAllWindows()

print("done")
