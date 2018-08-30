import Tile


class Intelligence:
    def __init__(self, _grid):
        self.grid = _grid
        self.analyse()

    def analyse(self):

        # Get tiles in each column
        # Set tile.accessible to number of moves required to grab that tile (1,2,5)
        chains = []
        for c in range(7):
            tile_column = self.grid.get_tile_column(c)
            l = len(tile_column)

            if l > 0:
                tile_column[0].accessible = 1
                if l > 1:
                    tile_column[1].accessible = 2
                    if l > 2:
                        tile_column[2].accessible = 5
        chain_id = 0
        for t in self.grid.tiles[::-1]:
            if t:
                if not t.pip:
                    if t.chained == -1:
                        t.chained = chain_id
                        current = Chain(t.colour)
                        current.append(t)
                        checks = list(t.neighbours.values()) + []
                        for n in checks:
                            if n:
                                if not n.pip and n.chained == -1 and n.colour == t.colour:
                                    n.chained = chain_id
                                    current.append(n)
                                    checks.extend(list(n.neighbours.values()))
                        chains.append(current)
                        chain_id += 1

        worthy_chunks = []
        for ch in chains:
            # print(ch)
            if min([x.accessible for x in ch.tiles]) > 5:
                # most accessible tile is at least 4 levels down (t.accessible = 99)
                # print("access-fail")
                continue
            needed = 4 - len(ch)

            if needed <= 0:
                raise ValueError('Score is 0 or negative somehow')

            if len(self.grid.tiles_of_colour[ch.colour]) < needed:
                # Not enough of that colour on the screen
                # print("notenoughcols-fail")
                continue
            # Possible tiles to add to chunk (don't share the same column as the chunk)
            search = [t for t in self.grid.tiles_of_colour[ch.colour] if t.col not in [s.col for s in ch.tiles]]
            # print(f"{ch.colour} search:", search)

            if len(search) < needed:
                # Not enough of coloured-tiles that aren't below the chunk
                # print("notenoughcols2-fail")
                continue

            # Get easiest to access tiles
            search.sort(key=lambda x: x.accessible)
            ch.best_tiles = search[:needed]
            # Score is roughly based on how many J/K moves required to access chunk and grab needed tiles.
            ch.score = sum([t.accessible for t in ch.best_tiles]) + ch.tiles[0].accessible
            worthy_chunks.append(ch)
        # print("w_c:", worthy_chunks)

        worthy_chunks.sort(key=lambda x: x.score)
        if len(worthy_chunks) == 0:
            print("no winner!")
        else:
            print("winner: ------")
            print(worthy_chunks[0])
            print([t.index for t in worthy_chunks[0].best_tiles])
            if len(worthy_chunks) > 1:
                print("runner-up: -----")
                print(worthy_chunks[1])
                print([t.index for t in worthy_chunks[1].best_tiles])
                if len(worthy_chunks) > 2:
                    print("third-place: -----")
                    print(worthy_chunks[2])
                    print([t.index for t in worthy_chunks[2].best_tiles])

        # chains.
        return


class Chain:
    def __init__(self, _colour):
        self.colour = _colour
        # self.id = _id
        self.tiles = []
        self.min_accessible = None
        self.score = -1
        self.best_tiles = []

    def sort(self):
        self.tiles.sort(key=lambda x: x.accessible)

    def append(self, ele):
        if type(ele) != Tile.Tile:
            raise ValueError('Append. Chains must only contain Tiles.')
        self.tiles.append(ele)

    def verbose_print(self):
        if len(self.tiles) == 0:
            _id = -1
        else:
            _id = self.tiles[0].chained
        return f"<{self.colour.capitalize()} Chain #{_id} | len={len(self)} | score={self.score} | {[t.index for t in self.tiles]}>"

    def __len__(self):
        return len(self.tiles)

    def __repr__(self):
        if len(self.tiles) == 0:
            _id = -1
        else:
            _id = self.tiles[0].chained
        return f"<{self.colour.capitalize()} Chain #{_id} | len={len(self)} | score={self.score} | {[t.index for t in self.tiles]}>"