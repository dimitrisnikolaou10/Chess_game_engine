from Piece import Piece


class Bishop(Piece):

    def is_valid(self, file, rank):
        old_file = self.file
        old_rank = self.rank
        new_file = file
        new_rank = rank
        df = abs(new_file - old_file)  # note the absolute value in this case
        dr = abs(new_rank - old_rank)

        if (old_file == new_file) and (old_rank == new_rank):  # if there is no move, flag up
            return False

        if df != dr:
            return False
        else:
            return True
