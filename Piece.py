class Piece:

    def __init__(self, colour, file, rank):
        self.colour = colour
        self.file = file
        self.rank = rank

    def move(self, file, rank):
        self.file = file
        self.rank = rank
