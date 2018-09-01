import time

import Settings
from directkeys import PressKey, ReleaseKey, J, K, LEFT, RIGHT


class Player:
    def __init__(self):
        self.pos = Settings.PLAYER_POS
        self.command_str = ""
        self.key_names = {"l": LEFT, "r": RIGHT, "g": J, "s": K}

    def move_to(self, _target):
        dx = _target - self.pos
        if dx > 0:
            self.command_str += "r" * dx
        elif dx < 0:
            self.command_str += "l" * (-dx)
        self.pos = _target

    def execute(self):
        # Temporary fix for 'left, right' 'right, left' over-moving?
        while "rl" in self.command_str or "lr" in self.command_str:
            self.command_str = self.command_str.replace("rl", "")
            self.command_str = self.command_str.replace("lr", "")

        for char in self.command_str:
            k = self.key_names[char]
            PressKey(k)
            time.sleep(Settings.DELTA)
            ReleaseKey(k)
            time.sleep(Settings.DELTA)
            if char == "s":
                time.sleep(0.5)  # Settings.DELTA*2)
        self.command_str = ""
        #print(f"I think I'm in POSITION {self.pos}.")

    def grab(self):
        self.command_str += "g"

    def drop(self):
        self.command_str += "g"

    def switch(self):
        self.command_str += "s"

    def left(self):
        self.command_str += "l"

    def right(self):
        self.command_str += "r"
