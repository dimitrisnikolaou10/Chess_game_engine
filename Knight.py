from Piece import Piece


class Knight(Piece):

    def is_valid(self, file, rank):
        old_file = self.file
        old_rank = self.rank
        new_file = file
        new_rank = rank
        df = abs(new_file - old_file)  # note the absolute value in this case
        dr = abs(new_rank - old_rank)

        if (old_file == new_file) and (old_rank == new_rank):  # if there is no move, flag up
            return False

        if dr == 2:
            if df == 1:
                return True
            else:
                return False

        if df == 2:
            if dr == 1:
                return True
            else:
                return False

        return False
