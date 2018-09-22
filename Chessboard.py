import numpy as np
from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King


class Chessboard:

    def __init__(self):

        print("New game is starting.")

        self.turn = 0
        self.end_game = 0

        self.board = np.empty((8, 8), dtype=object)
        for i in range(8):
            self.board[1][i] = Pawn(0, i, 1)  # populate with White Pawns
            self.board[6][i] = Pawn(1, i, 6)  # populate with Black Pawns

        # Rooks
        self.board[0][0] = Rook(0, 0, 0)  # first White Rook
        self.board[0][7] = Rook(0, 7, 0)  # second White Rook
        self.board[7][0] = Rook(1, 0, 7)  # first Black Rook
        self.board[7][7] = Rook(1, 7, 7)  # second Black Rook

        # Knights
        self.board[0][1] = Knight(0, 1, 0)  # first White Knight
        self.board[0][6] = Knight(0, 6, 0)  # second White Knight
        self.board[7][1] = Knight(1, 1, 7)  # first Black Knight
        self.board[7][6] = Knight(1, 6, 7)  # second Black Knight

        # Bishops
        self.board[0][2] = Bishop(0, 2, 0)  # first White Bishop
        self.board[0][5] = Bishop(0, 5, 0)  # second White Bishop
        self.board[7][2] = Bishop(1, 2, 7)  # first Black Bishop
        self.board[7][5] = Bishop(1, 5, 7)  # second Black Bishop

        # Queens
        self.board[0][3] = Queen(0, 3, 0)  # White Queen
        self.board[7][3] = Queen(1, 3, 7)  # Black Queen

        # Kings
        self.board[0][4] = King(0, 4, 0)  # White King
        self.board[7][4] = King(1, 4, 7)  # Black King

        # Booleans to indicate if a king is in check
        self.white_check = 0
        self.black_check = 0

    def reset_board(self):

        print("New game is starting.")

        self.turn = 0
        self.end_game = 0

        self.board = np.empty((8, 8), dtype=object)
        for i in range(8):
            self.board[1][i] = Pawn(0, i, 1)  # populate with White Pawns
            self.board[6][i] = Pawn(1, i, 6)  # populate with Black Pawns

        # Rooks
        self.board[0][0] = Rook(0, 0, 0)  # first White Rook
        self.board[0][7] = Rook(0, 7, 0)  # second White Rook
        self.board[7][0] = Rook(1, 0, 7)  # first Black Rook
        self.board[7][7] = Rook(1, 7, 7)  # second Black Rook

        # Knights
        self.board[0][1] = Knight(0, 1, 0)  # first White Knight
        self.board[0][6] = Knight(0, 6, 0)  # second White Knight
        self.board[7][1] = Knight(1, 1, 7)  # first Black Knight
        self.board[7][6] = Knight(1, 6, 7)  # second Black Knight

        # Bishops
        self.board[0][2] = Bishop(0, 2, 0)  # first White Bishop
        self.board[0][5] = Bishop(0, 5, 0)  # second White Bishop
        self.board[7][2] = Bishop(1, 2, 7)  # first Black Bishop
        self.board[7][5] = Bishop(1, 5, 7)  # second Black Bishop

        # Queens
        self.board[0][3] = Queen(0, 3, 0)  # White Queen
        self.board[7][3] = Queen(1, 3, 7)  # Black Queen

        # Kings
        self.board[0][4] = King(0, 4, 0)  # White King
        self.board[7][4] = King(1, 4, 7)  # Black King

        # Booleans to indicate if a king is in check
        self.white_check = 0
        self.black_check = 0

    def submit_move(self, start, end):

        if self.end_game:
            print("The game has ended.")
            return False

        if (len(start) > 2) or (len(end) > 2):
            print("Invalid submission of a move.")
            return False

        start_file = translate(start[0])  # translate from string to index - could have used ASCII conversion instead
        if start_file == -1:
            print("Invalid submission of a move.")
            return False
        start_rank = int(start[1])-1
        if (start_rank < 0) and (start_rank > 7):
            print("Invalid submission of a move.")
            return False

        end_file = translate(end[0])  # translate from string to index - could have used ASCII conversion instead
        if end_file == -1:
            print("Invalid submission of a move.")
            return False
        end_rank = int(end[1])-1
        if (end_rank < 0) and (end_rank > 7):
            print("Invalid submission of a move.")
            return False

        piece = self.board[start_rank][start_file]

        if piece is None:  # if there is no piece at the selected location
            print("There is no piece at the selected location")
            return False

        if piece.colour:
            if not self.turn:
                print("It is White's turn")
                return False
        else:
            if self.turn:
                print("It is Black's turn")
                return False

        if not piece.is_valid(end_file, end_rank):  # check if the piece can physically go there
            print("The piece selected cannot go there")
            return False

        if not self.is_not_obstructed(self.board, start_file, start_rank, end_file, end_rank):
            print("This move cannot be completed, it is obstructed by another piece.")
            return False

        if self.king_in_check(start_file, start_rank, end_file, end_rank):
            print("Can't move there, your king is/will be in check")
            return False

        self.move(start_file, start_rank, end_file, end_rank)

        if self.checks_other_king(piece.colour):
            col = 'White' if not piece.colour else 'Black'
            opp_col = 'Black' if piece.colour else 'White'
            if self.is_check_mate(piece.colour):
                self.end_game = 1
                print('The ' + col + ' team has won.')
            else:
                self.end_game = 1
                print('The ' + opp_col + ' King is in Check')

        if self.turn:
            self.turn = 0
        else:
            self.turn = 1

        return True

    def is_not_obstructed(self, board, start_file, start_rank, end_file, end_rank):

        piece = board[start_rank][start_file]
        piece_colour = piece.colour
        final_square = board[end_rank][end_file]

        if (start_file == end_file) and (start_rank == end_rank):
            return False

        # For all different type of pieces, check if path is blocked
        if type(piece) == Rook:
            if start_file != end_file:  # if it is a horizontal move
                for i in range(start_file + 1, end_file):  # check until second to last box
                    next_square = board[start_rank][i]  # start rank assumed to be same as end rank
                    if next_square is not None:
                        return False
            elif start_rank != end_rank:  # if it is a vertical move
                for i in range(start_rank + 1, end_rank):  # check until second to last box
                    next_square = board[i][start_file]  # start file assumed to be same as end file
                    if next_square is not None:
                        return False

        if type(piece) == Bishop:
            for j, i in zip(range(start_file + 1, end_file), range(start_rank + 1, end_rank)):
                next_square = board[i][j]
                if next_square is not None:
                    return False

        if type(piece) == Queen:
            if (start_file != end_file) and (start_rank == end_rank):  # if it is a horizontal move
                for i in range(start_file + 1, end_file):  # check until second to last box
                    next_square = board[start_rank][i]  # start rank is same as end rank
                    if next_square is not None:
                        return False
            elif (start_rank != end_rank) and (start_file == end_file):  # if it is a vertical move
                for i in range(start_rank + 1, end_rank):  # check until second to last box
                    next_square = board[i][start_file]  # start file is same as end file
                    if next_square is not None:
                        return False
            else:
                for j, i in zip(range(start_file + 1, end_file), range(start_rank + 1, end_rank)):
                    next_square = board[i][j]
                    if next_square is not None:
                        return False

        # check what the final square consists of
        # covers the case of King, Pawn and Knight entirely and all the rest partially
        if final_square is None:
            return True
        elif final_square.colour != piece_colour:
            return True
        else:
            return False

    def king_in_check(self, start_file, start_rank, end_file, end_rank):

        piece = self.board[start_rank][start_file]
        piece_colour = piece.colour

        new_board = self.board.copy()  # make a copy of the board and make the changes on that

        new_board[start_rank][start_file] = None
        new_board[end_rank][end_file] = piece

        king_file, king_rank = -1, -1
        for r in range(8):
            for f in range(8):
                if new_board[r][f] is None:
                    continue
                elif (new_board[r][f].colour == piece_colour) and (type(new_board[r][f]) == King):
                    king_rank = r
                    king_file = f

        for r in range(8):
            for f in range(8):
                next_piece = new_board[r][f]
                if next_piece is None:
                    continue
                elif next_piece.colour == piece_colour:
                    continue
                else:
                    if (next_piece.is_valid(king_file, king_rank)) and (self.is_not_obstructed(new_board, f, r, king_file, king_rank)):
                        return True

        return False

    def move(self, start_file, start_rank, end_file, end_rank):

        piece = self.board[start_rank][start_file]
        self.board[start_rank][start_file] = None
        self.board[end_rank][end_file] = piece

        piece.file = end_file
        piece.rank = end_rank

        return

    def checks_other_king(self, colour):

        king_file, king_rank = -1, -1
        for r in range(8):
            for f in range(8):
                if self.board[r][f] is None:
                    continue
                if (self.board[r][f].colour != colour) and (type(self.board[r][f]) == King):
                    king_rank = r
                    king_file = f

        for r in range(8):
            for f in range(8):
                if self.board[r][f] is None:
                    continue
                next_piece = self.board[r][f]
                if next_piece.colour != colour:
                    continue
                else:
                    if (next_piece.is_valid(king_file, king_rank)) and (self.is_not_obstructed(self.board, f, r, king_file, king_rank)):
                        return True

        return False

    def is_check_mate(self, colour):

        king_file, king_rank = -1, -1
        for r in range(8):
            for f in range(8):
                next_piece = self.board[r][f]
                if next_piece is None:
                    continue
                if (next_piece.colour != colour) and (type(next_piece) == King):
                    king_rank = r
                    king_file = f

        # check if any of the 8 possible moves are valid
        valid_moves = 0
        if self.check_if_valid_move(king_file, king_rank, king_file, king_rank + 1, colour):
            valid_moves += 1
        elif self.check_if_valid_move(king_file, king_rank, king_file, king_rank - 1, colour):
            valid_moves += 1
        elif self.check_if_valid_move(king_file, king_rank, king_file + 1, king_rank + 1, colour):
            valid_moves += 1
        elif self.check_if_valid_move(king_file, king_rank, king_file - 1, king_rank + 1, colour):
            valid_moves += 1
        elif self.check_if_valid_move(king_file, king_rank, king_file + 1, king_rank - 1, colour):
            valid_moves += 1
        elif self.check_if_valid_move(king_file, king_rank, king_file - 1, king_rank - 1, colour):
            valid_moves += 1
        elif self.check_if_valid_move(king_file, king_rank, king_file + 1, king_rank, colour):
            valid_moves += 1
        elif self.check_if_valid_move(king_file, king_rank, king_file + 1, king_rank, colour):
            valid_moves += 1

        if valid_moves:
            return False
        else:
            return True

    def check_if_valid_move(self, file, rank, new_file, new_rank, colour):

        new_board = self.board.copy()

        if (new_file > 7) or (new_file < 0) or (new_rank > 7) or (new_rank < 0):
            return False

        if not self.is_not_obstructed(new_board, file, rank, new_file, new_rank):
            return False

        static_move(new_board, file, rank, new_file, new_rank)

        if static_checks_other_king(new_board, colour):
            return False

        return True


def static_move(board, start_file, start_rank, end_file, end_rank):

        piece = board[start_rank][start_file]
        board[start_rank][start_file] = None
        board[end_rank][end_file] = piece

        return


def static_checks_other_king(board, colour):

    king_file, king_rank = -1, -1
    for r in range(8):
        for f in range(8):
            if board[r][f] is None:
                continue
            if (board[r][f].colour != colour) and (type(board[r][f]) == King):
                king_rank = r
                king_file = f

    for r in range(8):
        for f in range(8):
            if board[r][f] is None:
                continue
            next_piece = board[r][f]
            if next_piece.colour != colour:
                continue
            else:
                if next_piece.is_valid(king_file, king_rank):
                    return True

    return False


def translate(letter):
    if letter == 'A':
        return 0
    elif letter == 'B':
        return 1
    elif letter == 'C':
        return 2
    elif letter == 'D':
        return 3
    elif letter == 'E':
        return 4
    elif letter == 'F':
        return 5
    elif letter == 'G':
        return 6
    elif letter == 'H':
        return 7
    else:
        return -1
