import Settings
import Tile


class Intelligence:
    def __init__(self, _grid, _player):
        self.grid = _grid
        self.pos = Settings.PLAYER_POS
        self.player = _player

    def set_accessiblity(self):
        # Get tiles in each column
        # Set tile.accessible to number of moves required to grab that tile (1,2,5,7)
        for c in range(7):
            tile_column = self.grid.get_tile_column(c)
            l = len(tile_column)

            if l > 0:
                tile_column[0].accessible = 1
                if l > 1:
                    tile_column[1].accessible = 2
                    if l > 2:
                        tile_column[2].accessible = 5
                        if l > 3:
                            tile_column[3].accessible = 7

    def get_chains(self):
        chains = []
        chain_id = 0
        for t in self.grid.tiles[::-1]:
            if t:
                if not t.pip and t.chained == -1:
                    t.chained = chain_id
                    current = Chain(t.colour)
                    current.append(t)
                    checks = list(t.neighbours.values())
                    for n in checks:
                        if n:
                            if n.chained == -1 and n.colour == t.colour and not n.pip:
                                n.chained = chain_id
                                current.append(n)
                                checks.extend(n.neighbours.values())
                    chains.append(current)
                    chain_id += 1
        return chains

    def get_best_chain(self, _chains, _target_chunk_size):
        worthy_chains = []
        for ch in _chains:
            needed = _target_chunk_size - len(ch)
            if needed <= 0:
                raise ValueError('Score is 0 or negative somehow')

            if len(self.grid.tiles_of_colour[ch.colour]) < needed:
                # Not enough of that colour on the screen
                continue

            # Possible tiles to add to chunk (that don't share the same column as the chunk)
            search = [t for t in self.grid.tiles_of_colour[ch.colour] if t.col not in [s.col for s in ch.tiles]]
            if len(search) < needed:
                # Not enough of coloured-tiles that aren't below the chunk
                continue

            # Get easiest to access tiles
            search.sort(key=lambda x: x.accessible)
            ch.best_tiles = search[:needed]
            # Score is roughly based on how many J/K moves required to access chunk and grab needed tiles.
            ch.score = sum([t.accessible for t in ch.best_tiles]) + ch.tiles[0].accessible
            worthy_chains.append(ch)

        winner = None
        worthy_chains.sort(key=lambda x: x.score)

        if len(worthy_chains) > 0:
            if any([t.accessible > 7 for t in worthy_chains[0].best_tiles]):
                return None
            else:
                winner = worthy_chains[0]
                winner.tiles.sort(key=lambda t: t.accessible)
                print("Winner: ", winner)
                # if len(worthy_chains) > 1:
                #     print("runner-up: -----")
                #     print(worthy_chains[1])
                #     if len(worthy_chains) > 2:
                #         print("third-place: -----")
                #         print(worthy_chains[2])
        return winner

    def analyse(self):

        self.set_accessiblity()

        all_chains = self.get_chains()
        chains = []
        for ch in all_chains:
            # Filter out chains that can't be accessed
            if min([x.accessible for x in ch.tiles]) <= 7:
                chains.append(ch)

        winner = self.get_best_chain(chains, 4)
        if not winner:

            winner = self.get_best_chain(chains, 3)
            if winner:
                print("FOUND A 3-CHAIN. 333")
            else:
                winner = self.get_best_chain(chains, 2)
                if winner:
                    print("FOUND A 2-CHAIN. 22")
        return winner

    def move(self, winner):
        #print(f"MOVEMENT = {Settings.MOVEMENT}")

        access_tile = winner.tiles[0]
        columns_of_loose = [t.col for t in winner.best_tiles]

        # Move to column (Waste-full if chunk is already accessible)
        self.player.move_to(access_tile.col)

        if access_tile.accessible != 1:
            # Clear space for other tiles
            # distances = [c - access_tile.col for c in range(7) if c not in columns_of_loose]
            untaken_cols = [c for c in range(7) if c not in columns_of_loose + [access_tile.col]]
            distance_sorted = sorted(untaken_cols, key=lambda c: abs(c - access_tile.col))
            dumping_col = distance_sorted[0]
            # if len(distances) == 0:
            #    print("No dumping column found. How is this possible?")
            # distances = [x for x in distances if x != 0]
            # distances.sort(key=lambda x: abs(x))
            # dumping_col = distances[0]
            # dx = dumping_col


            # col_heights = [999 if c in columns_of_loose else len(self.grid.get_tile_column(c)) for c in range(7)]
            # print("-"*20)
            # print(col_heights)
            # _target = col_heights.index(min(col_heights))
            # dx = _target - pos
            # Dump blocking tile elsewhere and move back
            if access_tile.accessible == 2:
                repeat = 1
            elif access_tile.accessible == 5:
                repeat = 2
            elif access_tile.accessible == 7:
                repeat = 3
            else:
                print(f"acc_tile.accessible = {access_tile.accessible}")
                raise ValueError(f"acc_tile.accessible = {access_tile.accessible}")

            for _ in range(repeat):
                self.player.grab()
                self.player.move_to(dumping_col)
                self.player.drop()
                self.player.move_to(access_tile.col)

            # Chunk should now be accessible.

        # Pick up loose tiles
        for target in winner.best_tiles:
            if target.accessible > 7:
                # Should not happen now
                raise IndexError(f"Target tile.accessible is {target.accessible}. Score of chunk = {winner.score}.")

            self.player.move_to(target.col)

            if target.accessible == 2:
                self.player.switch()
            elif target.accessible == 5:
                self.player.grab()
                self.player.switch()
                self.player.drop()
                self.player.switch()
            elif target.accessible == 7:
                print("digging")
                # best tile is deep down- do some digging
                # TODO: Fix - possible to dump tiles and block the chunk here...
                if target.col != 0:
                    self.player.command_str += "glgrgsgs"
                else:
                    self.player.command_str += "grglgsgs"

            self.player.grab()
            self.player.move_to(access_tile.col)
            self.player.drop()

        # Keep track of location. (No need to return to centre - debugging purposes only)
        Settings.PLAYER_POS = access_tile.col

        if Settings.MOVEMENT:
            self.player.execute()


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

    def __len__(self):
        return len(self.tiles)

    def __repr__(self):
        if len(self.tiles) == 0:
            _id = -1
        else:
            _id = self.tiles[0].chained
        return f"<{self.colour.capitalize()} Chain #{_id} | len={len(self)} | score={self.score} | {[t.index for t in self.tiles]} | {[t.index for t in self.best_tiles]}>"
