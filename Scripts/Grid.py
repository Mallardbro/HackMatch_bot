class Grid:
    def __init__(self):
        # pre_tiles to be populated with found tiles
        self.pre_tiles = []
        # tiles to be populated with pre_tiles and None for correct indexing.
        self.tiles = [None] * 70
        self.tiles_of_colour = {'red': [], 'green': [], 'orange': [], 'pink': [],
                                'violet': []}

    def setup_tiles(self):
        # To be called when pre_tiles is filled with all of the found tiles
        # Set row of tiles ('normalise' y by subtracting minimum.)
        min_y = min([t.iy for t in self.pre_tiles])
        for t in self.pre_tiles:
            t.row = int(round((t.iy - min_y) / 100))
            t.set_index()
            self.tiles[t.index] = t
            if not t.pip:
                self.tiles_of_colour[t.colour].append(t)

        # Fix for top row being incomplete (matching patterns for some but not whole row)
        if None in self.get_row(0):
            self.tiles = self.tiles[7:] + [None] * 7
            for i, t in enumerate(self.tiles):
                if t:
                    t.index = i
                    t.row -= 1

        self.init_neighbours()
        # print("Grid set up.")
        return

    def init_neighbours(self):
        for t in self.tiles:
            if not t:
                continue
            if t.row != 0:
                t.neighbours["up"] = self.tiles[t.index - 7]
            if t.row != 9:
                t.neighbours["down"] = self.tiles[t.index + 7]
            if t.col != 0:
                t.neighbours["left"] = self.tiles[t.index - 1]
            if t.col != 6:
                t.neighbours["right"] = self.tiles[t.index + 1]
        return

    def check_set_up(self):
        if len([t for t in self.tiles]) == 0:
            raise ValueError('Grid is not set up.')

    def get_row(self, num):
        self.check_set_up()
        return self.tiles[num * 7:num * 7 + 7]

    def get_column(self, num):
        self.check_set_up()
        return self.tiles[num::7]

    def get_tile_column(self, num):
        # Removes leading None elements from columns.
        c = self.get_column(num)[::-1]
        i = 0
        for t in c:
            if not t:
                i += 1
            else:
                break
        return c[i:]

    def draw(self, _image, _mode="rgb"):
        self.check_set_up()
        for t in self.tiles:
            if t:
                t.draw(_image, _mode)

    def __repr__(self):
        self.check_set_up()
        out = "#|--0-|--1-|--2-|--3-|--4-|--5-|--6-|"
        for r in range(10):
            out += "\n" + str(r) + "|" + "|".join(map(str, self.get_row(r))) + "|"
        return out
