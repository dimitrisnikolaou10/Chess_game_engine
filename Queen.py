from Piece import Piece


class Queen(Piece):

    def is_valid(self, file, rank):
        old_file = self.file
        old_rank = self.rank
        new_file = file
        new_rank = rank
        df = abs(new_file - old_file)  # note the absolute value in this case
        dr = abs(new_rank - old_rank)

        if (old_file == new_file) and (old_rank == new_rank):  # if there is no move, flag up
            return False

        if df > 0:  # if rank has changed
            if df == dr:  # queen must have moved diagonally
                return True
            elif dr == 0:  # or straight
                return True
            else:
                return False

        if dr > 0:  # equivalent to above
            if dr == df:
                return True
            elif df == 0:
                return True
            else:
                return False
