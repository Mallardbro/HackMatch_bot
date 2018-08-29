class Grid:
    def __init__(self):
        # pre_tiles to be populated with found tiles
        self.pre_tiles = []
        # tiles to be populated with pre_tiles and None for correct indexing.
        self.tiles = []
        self.set_up = False

    def setup_tiles(self):
        # To be called when pre_tiles is filled with all of the found tiles
        # Set row of tiles ('normalise' y by subtracting minimum.)
        min_y = min([t.iy for t in self.pre_tiles])
        for t in self.pre_tiles:
            t.row = int(round((t.iy - min_y) / 100))
            t.set_index()

        self.tiles = [None] * 70
        for t in self.pre_tiles:
            self.tiles[t.index] = t
        self.set_up = True
        print("Grid set up.")

    def check_set_up(self):
        if not self.set_up:
            raise ValueError('Grid is not set up.')

    def get_row(self, num):
        self.check_set_up()
        return self.tiles[num * 7:num * 7 + 7]

    def get_column(self, num):
        self.check_set_up()
        return self.tiles[num::7]

    def draw(self, _image):
        self.check_set_up()
        for t in self.tiles:
            if t:
                t.draw(_image)

    def __repr__(self):
        self.check_set_up()
        out = "#|--0-|--1-|--2-|--3-|--4-|--5-|--6-|"
        for r in range(10):
            out += "\n" + str(r) + "|" + "|".join(map(str, self.get_row(r))) + "|"
        return out
