import time

import Settings
import Tile
from directkeys import PressKey, ReleaseKey, LEFT, RIGHT, J, K


class Intelligence:
    def __init__(self, _grid):
        self.grid = _grid
        # w = self.analyse()
        # self.move(w)
        self.pos = Settings.PLAYER_POS
    def analyse(self):

        # Get tiles in each column
        # Set tile.accessible to number of moves required to grab that tile (1,2,5)
        chains = []
        for c in range(7):
            tile_column = self.grid.get_tile_column(c)
            l = len(tile_column)
            #print(tile_column)
            if l > 0:
                tile_column[0].accessible = 1
                if l > 1:
                    tile_column[1].accessible = 2
                    if l > 2:
                        tile_column[2].accessible = 5
                        if l > 3:
                            tile_column[3].accessible = 7
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
            #print(ch)
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
        winner = None
        worthy_chunks.sort(key=lambda x: x.score)
        # if len(worthy_chunks) == 0:
        # print("no winner!")
        if len(worthy_chunks) > 0:
            winner = worthy_chunks[0]
            print("Winner: ", winner)
            # if len(worthy_chunks) > 1:
            #     print("runner-up: -----")
            #     print(worthy_chunks[1])
            #     print([t.index for t in worthy_chunks[1].best_tiles])
            #     if len(worthy_chunks) > 2:
            #         print("third-place: -----")
            #         print(worthy_chunks[2])
            #         print([t.index for t in worthy_chunks[2].best_tiles])
        return winner

    def move(self, winner):
        print("Movement!")
        key_names = {"left": LEFT, "right": RIGHT, "grab": J, "switch": K}
        commands = []
        access_tile = winner.tiles[0]
        columns_of_loose = [t.col for t in winner.best_tiles]
        # TODO - if one needs removing, just grab and switch
        # TODO - what if loose tiles are in the same column!?
        # TODO - check for ...left, right...s in commands

        # Move to column ("Waste full if chunk is already accessible)
        dx = access_tile.col - self.pos
        dx_save = dx
        if dx > 0:
            commands.extend(["right"] * dx)
        elif dx < 0:
            commands.extend(["left"] * (-1 * dx))

        self.pos = access_tile.col

        if access_tile.accessible != 1:
            # Clear space for other tiles
            #print("clear below chunk")
            # Pickup blocking tile
            commands.append("grab")

            distances = [c - access_tile.col for c in range(7) if c not in columns_of_loose]
            if len(distances) == 0:
                print("No dumping column found. How is this possible?")
            distances = [x for x in distances if x != 0]
            distances.sort(key=lambda x: abs(x))
            dumping_col = distances[0]
            dx = dumping_col

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
            else:
                raise ValueError(f"acc_tile.accessible = {access_tile.accessible}")

            for _ in range(repeat):
                if dx > 0:
                    commands.extend(["right"] * dx)
                    commands.append("grab")
                    commands.extend(["left"] * dx)
                elif dx < 0:
                    commands.extend(["left"] * (-1 * dx))
                    commands.append("grab")
                    commands.extend(["right"] * (-1 * dx))


            # chunk should now be accessible
        # Uncovered
        # pick up tiles
        #print("best tiles:", winner.best_tiles)
        for target in winner.best_tiles:
            if (target.accessible > 7):
                print("----------------------------------")
                print("-----------t.a > 7----------------")
                print("----------------------------------")
                print("----------------------------------")

            dx = target.col - self.pos
            if target.col > self.pos:
                commands.extend(["right"] * dx)
                if target.accessible == 2:
                    commands.append("switch")
                elif target.accessible == 5:
                    commands.extend(["grab", "switch", "grab", "switch"])
                elif target.accessible == 7:
                    print("digging")
                    # best tile is deep down- do some digging
                    if target.col != 0:
                        commands.extend(["grab", "left", "grab", "right", "grab", "switch", "grab", "switch"])
                    else:
                        commands.extend(["grab", "right", "grab", "left", "grab", "switch", "grab", "switch"])
                commands.append("grab")
                commands.extend(["left"] * dx)
                commands.append("grab")
            elif target.col < self.pos:
                commands.extend(["left"] * (-dx))
                if target.accessible == 2:
                    commands.append("switch")
                elif target.accessible == 5:
                    commands.extend(["grab", "switch", "grab", "switch"])
                elif target.accessible == 7:
                    print("digging")
                    # best tile is deep down- do some digging
                    if target.col != 0:
                        commands.extend(["grab", "left", "grab", "right", "grab", "switch", "grab", "switch"])
                    else:
                        commands.extend(["grab", "right", "grab", "left", "grab", "switch", "grab", "switch"])
                commands.append("grab")
                commands.extend(["right"] * (-dx))
                commands.append("grab")

        # Return to centre
        # commands.extend(["left"] * 6)
        # commands.extend(["right"] * 3)
        Settings.PLAYER_POS = access_tile.col

        if Settings.MOVEMENT:
            for do in commands:
                # if do == "noop":
                #    time.sleep(Settings.DELTA)

                k = key_names[do]
                PressKey(k)
                time.sleep(Settings.DELTA)
                ReleaseKey(k)
                time.sleep(Settings.DELTA)
                if do == "switch":
                    time.sleep(Settings.DELTA)
        else:
            print("MOVEMENT = FALSE")

        print(commands)


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
