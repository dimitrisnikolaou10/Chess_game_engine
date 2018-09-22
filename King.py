from Piece import Piece


class King(Piece):

    def is_valid(self, file, rank):
        old_file = self.file
        old_rank = self.rank
        new_file = file
        new_rank = rank
        df = abs(new_file - old_file)  # note the absolute value in this case
        dr = abs(new_rank - old_rank)

        if (old_file == new_file) and (old_rank == new_rank):  # if there is no move, flag up
            return False

        if (df > 1) or (dr > 1):
            return False

        if df > 0:
            if (dr != 0) and (dr != 1):
                return False

        if dr > 0:
            if (df != 0) and (df != 1):
                return False

        return True
