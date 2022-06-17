# [[file:checker.org::*questions][questions:1]]
# !/usr/bin/env python3

#Group: Thomas Moraes, Dante Ricketts, Steven Zhivov



from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
from easyAI import solve_with_iterative_deepening
import numpy as np

# black_square
even = [0,2,4,6]
odd = [1,3,5,7]

# init
even_row = [(i,j) for i in even for j in odd]
odd_row = [(i,j) for i in odd for j in even]

black_squares = even_row + odd_row

#Checker is a subclass of TwoPlayerGame?
class Checker(TwoPlayerGame):

    #class initializer
    def __init__(self, players):
        self.players = players
        # self.board = np.arange(8 * 8).reshape(8,8)
        #initializing the board with blanks
        self.blank_board = np.zeros((8,8), dtype=object)
        self.board = self.blank_board.copy()
        #initializing black pieces
        self.black_pieces = [
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]
        #initializing white pieces
        self.white_pieces = [
            (6,1), (6,3), (6,5), (6,7),
            (7,0), (7,2), (7,4), (7,6)
        ]
        for i,j in self.black_pieces:
            self.board[i,j] = "B"
        for i,j in self.white_pieces:
            self.board[i,j] = "W"

        #declaring the territory to upgrade to KING
        self.white_territory = [(7,0), (7,2), (7,4), (7,6)]
        self.black_territory = [(0,1), (0,3), (0,5), (0,7)]

        #assigning list of pieces to each player
        self.players[0].pos = self.white_pieces
        self.players[1].pos = self.black_pieces

        self.current_player = 1  # player 1 starts.

    def possible_moves_on_white_turn(self):

        table_pos = []
        #will hold elements with 2 coordinate points (tuples) indicating current position and possible new positions
        old_new_piece_pos = []

        # board position before move
        # fills board with the current positions for W and B pieces
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            #checks for options for each white piece v
            old_piece_pos = v

            #steps are the diagonal moves without captures
            step_pos = [(v[0]-1, v[1]-1), (v[0]-1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                #checking if n is inside the board on a black square
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    #if there's a B or W piece in position n, checks jump positions
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        #checks if the jump position is empty (has no piece in it)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        #appends possible jump position to the possible moves array
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        #adds a possible position to move
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move
        for i,j in old_new_piece_pos:
            #print(f"i = {i}")
            b = board.copy()
            b[i[0], i[1]] = 0 # old position
            b[j[0], j[1]] = "W" # new position
            # print(b)
            #table_pos stores all possible board positions after a move
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_white_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        #saves board
        self.board = board
        return table_pos

    def possible_moves_on_black_turn(self):
        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]+1, v[1]-1), (v[0]+1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move

        for i,j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = 0
            b[j[0], j[1]] = "B"
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_black_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos

    def possible_moves(self):
        """
        """

        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()

    def get_piece_pos_from_table(self, table_pos):
        if self.current_player-1 == 0:
            x = np.where(table_pos == "W")
        elif self.current_player-1 == 1:
            x = np.where(table_pos == "B")
        else:
            raise ValueError("There can be at most 2 players.")

        assert len(np.where(table_pos != 0)[0]) == 16, f"In get_piece_pos_from_table(), there are {len(np.where(table_pos != 0)[0])} pieces on the board  \n {table_pos}"
        return [(i,j) for i,j in zip(x[0], x[1])]

    def make_move(self, pos):

        #updating player position with a new move
        #pos is a move coordinate
        self.player.pos = self.get_piece_pos_from_table(pos)

        pass

    def lose(self):
        """
        check if W on B territory return 1
        else check if B on W territory return 2
        else return 0 (not over)
        """

        #conditions for not having possible moves
        #apparently the function call doesn't work
        #if (self.possible_moves() == []):
        #    if (self.current_player == 1):
        #        print("Black won")
        #        return 1
        #   if (self.current_player == 2):
        #        print("White won")
        #        return 1
        
        #conditions for territories
        for (i, j) in self.black_territory:
            if self.board[i, j] == "W":
                print("White won")
                return 1
        for (i, j) in self.white_territory:
            if self.board[i, j] == "B":
                print("Black won")
                return 1

        return 0

    def is_over(self):
        """
        game is over immediately when one player get one of its piece into opponent's territory.
        """
        #over when the lose function determines a loser and returns 1
        return (self.lose())

    def show(self):
        """
        show 8*8 checker board.
        """

        # board position before move
        board = self.blank_board.copy()
        print(f"player 1 positions = {self.players[0].pos}")
        print(f"player 2 positions = {self.players[1].pos}")
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        print('\n')
        print(board)

    def scoring(self):
        """
        win = 0
        lose = -100
        """
        #taken from tic-tac-toe. -100 when the game is over, and 0 when there is a win.
        #has to be 0 to keep the code from adding throughout the game
        return -100 if self.lose() else 0


if __name__ == "__main__":
    ai = Negamax(1) # The AI will think 13 moves in advance
    game = Checker( [ AI_Player(ai), AI_Player(ai) ] )
    history = game.play()
# questions:1 ends here