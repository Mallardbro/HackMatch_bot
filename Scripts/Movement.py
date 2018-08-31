class Player():
    def __init__(self):
        self.pos = 3
        self.command_str = ""

    def move_to(self, _target):
        dx = _target - self.pos
        if dx > 0:
            self.command_str += "r" * dx
        else:
            self.command_str += "l" * (-dx)
        self.pos = _target

    def grab(self):
        self.command_str += "g"

    def drop(self):
        self.command_str += "g"

    def switch(self):
        self.command_str += "s"

    def left(self):
        self.command_str += "l"

    def right(self)
        self.command_str += "r"
