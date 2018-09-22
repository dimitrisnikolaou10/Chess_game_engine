from Piece import Piece


class Pawn(Piece):

    def is_valid(self, file, rank):
        old_file = self.file
        old_rank = self.rank
        new_file = file
        new_rank = rank
        df = new_file - old_file
        dr = new_rank - old_rank

        if (old_file == new_file) and (old_rank == new_rank):  # if there is no move, flag up
            return False

        if self.colour:
            dr = dr * (-1)

        if (dr != 1) and (dr != 2):
            return False

        if abs(df) > 1:
            return False

        return True
