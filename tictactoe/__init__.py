import sys
import numpy as np
import math
import json

from numpy.core.numeric import isclose

inf = 9999999999
move_count = 0
ai_count = 0
player_count = 0
best_move_pos = [0, ()]


class Move:
    def __init__(self, key, symbol):
        self.key = key
        self.pos = {}
        self.pos_val = 0
        self.symbol = symbol

    def set_pos(self, pos, pos_key):

        self.pos[pos_key] = pos

    def set_val(self, val):

        self.pos_val = val

    def get_val(self):

        return self.pos_val

    def set_pos_val(self, pos, pos_key, val):
        try:
            pos[pos_key].set_val(val)
            return pos
        except:
            return False

    def get_pos_val(self, pos, pos_key):

        try:
            return pos[pos_key].pos_val
        except:
            return False

    def get_pos_symbol(self, pos, pos_key):

        try:
            return pos[pos_key].symbol
        except:
            return False

    def evaluate_move_pos(self, board):

        pass

    def get_pos(self, pos_key):

        try:
            return self.pos[pos_key]
        except:
            return False

    def set_symbol(self, symbol):

        self.symbol = symbol

    def get_symbol(self):

        return self.symbol


class Player:
    def __init__(self, attacking):

        self.attacking = attacking
        self.moves = {}

    def set_move(self, move, pos):

        self.moves[pos] = move

    def get_moves(self):

        return self.moves


class Board:
    def __init__(self):
        self.board = [
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
        ]

        self.board = np.array(self.board)
        self.evaluated_board = {}

        self.value_dict = {"X": 10, "tie": 5, "O": -10}
        self.reverse_symbol = {"O": "X", "X": "O"}
        self.len = len(self.board)
        self.available_moves = None
        self.direction = [
            "up",
            "down",
            "left",
            "right",
            "upright",
            "downleft",
            "upleft",
            "downright",
        ]

        self.tuple_direction = [
            ("up", "down"),
            ("left", "right"),
            ("upright", "downleft"),
            ("upleft", "downright"),
        ]

        self.new_directions = [
            "vertical",
            "horizontal",
            "diagonal_left",
            "diagonal_right",
        ]

    def get_evaluated_board(self):

        arr = {}
        for item in self.evaluated_board:
            arr[str(item)] = self.evaluated_board[item]

        return arr

    def equals(self, side, symbol):

        last_index = 0
        symbol = None
        ratio = 0
        info = {
            "X": 0,
            "O": 0,
        }

        for index in range(len(side)):

            if side[index] != "-":

                if symbol != side[index]:

                    start = index
                    symbol = side[index]
                    last_index = index
                    ratio = 1

                elif index == last_index + 1:

                    ratio += 1
                    last_index = index
                    info[symbol] = ratio

        return info

    def is_blocked(self, side, pos, symbol):

        side_len = len(side)
        if side_len < pos:

            return False

        if pos > 0:

            if side[pos - 1] == self.reverse_symbol[symbol]:

                return True

        if pos + 1 < side_len:

            if side[pos + 1] == self.reverse_symbol[symbol]:

                return True

        return False

    def evaluate_side(self, side, symbol, pos_key, direction):

        side = list(side)
        i, j = pos_key

        if i == 0 or j == 0:
            length = 0
        else:
            length = self.len - i if i > j else self.len - j

        is_corner = lambda x: True if x - 1 <= 2 or x + 1 >= 5 else False

        free_space = side.count("-")

        info = self.equals(side, symbol)

        count = info[symbol]
        reverse_count = info[self.reverse_symbol[symbol]]

        # count = abs(count - reverse_count)

        if is_corner(length) and info[symbol] != 3:

            ratio_corner = 0.8
            ratio = count * 2

        else:

            ratio_corner = 1
            ratio = count * 2 if count >= 2 else count

        val = ((ratio * ratio_corner) + free_space) / 10

        position = i if direction == "vertical" else j

        if self.is_blocked(side, position, symbol):

            val -= val / 5

        if count != 0 or reverse_count != 0:
            print(
                f"R {ratio} C {ratio_corner} L {length} F {free_space} V {val} I {info}"
            )

        return round(val, 3)

    def evaluate_board(self, play, symbol):

        best_play = None
        plays = self.ai_moves | self.player_moves
        av_moves = self.available_moves
        f = open("values.log", "a+")

        for move_key in plays:
            # print(f"MOVE {move_key}")
            move = plays[move_key]
            for pos in self.direction:

                pos_key = move.get_pos(pos)

                if pos_key:

                    symb = self.available_moves[pos_key].get_symbol()

                    for direction in self.new_directions:

                        if symb == "-":
                            side = self.get_board_arr(pos_key, direction)
                        else:
                            break

                        e_val = self.evaluate_side(side, symbol, pos_key, direction)
                        val = self.available_moves[pos_key].get_val()

                        # f.write(f"info : {pos_key} {pos} {direction} : {side} \n")
                        # f.write(f"values : {e_val} {val}\n")

                        if e_val < val:
                            e_val = val

                        self.available_moves = self.available_moves[
                            pos_key
                        ].set_pos_val(self.available_moves, pos_key, e_val)
                        self.evaluated_board[pos_key] = {"value": e_val}

                f.write("\n")

        for key in plays:
            self.evaluated_board[key] = {
                "value": None,
                "symbol": plays[key].get_symbol(),
            }

        f.close()
        # for item in self.evaluated_board:
        # print(f"Item : {item} {self.evaluated_board[item]}")
        # pass

        return self.available_moves

    def print_board_state(self):

        print("\n--------------------------------------------------\n")
        for row in self.board:
            print(row)
        print("\n--------------------------------------------------\n")

    def play(self, play, symbol, available_moves, ai_moves={}, player_moves={}):

        global move_count
        x, y = play
        if self.board[x][y] == "-":
            self.board[x][y] = symbol
            self.available_moves = available_moves
            self.ai_moves = ai_moves
            self.player_moves = player_moves

            return self.evaluate_board(play, symbol)

        raise ValueError("Casa já tem coisa.")

    def get_board_arr(self, pos, direction):

        if not pos:
            return []

        if direction == "horizontal":

            i, j = pos
            horizontal = self.board[i][0:]
            return horizontal

        if direction == "vertical":

            i, j = pos
            vertical = []
            for x in range(0, self.len):
                vertical.append(self.board[x][j])
            return vertical

        if direction == "diagonal_right":

            i, j = pos
            diagonal_right = []
            while i != 0 and j != 0:
                i -= 1
                j -= 1

            for x in range(i, self.len):
                try:
                    diagonal_right.append(self.board[x][j])
                except:
                    break
                j += 1
            return diagonal_right

        if direction == "diagonal_left":

            i, j = pos
            diagonal_left = []
            while i != 0 and j + 1 != self.len:
                i -= 1
                j += 1

            for x in range(j, -1, -1):
                try:
                    diagonal_left.append(self.board[i][x])
                except:
                    break
                i += 1

            return diagonal_left


class AI:
    def __init__(self, board, value_dict, board_len, attacking):

        self.board = board
        self.board_len = board_len
        self.value_dict = value_dict
        self.attacking = attacking
        self.moves = {}
        self.direction = [
            "up",
            "down",
            "left",
            "right",
            "upright",
            "downleft",
            "upleft",
            "downright",
        ]

    def get_moves(self):

        return self.moves

    def set_move(self, move, pos):

        self.moves[pos] = move

    def play(self, board, available_moves, player_moves):

        best_play = None
        plays = self.moves | player_moves
        for move_key in plays:
            move = plays[move_key]
            for pos in self.direction:
                pos_key = move.get_pos(pos)
                if pos_key:
                    if available_moves[pos_key].get_symbol() == "-":
                        val = available_moves[pos_key].get_val()
                        if best_play == None:
                            best_play = (pos_key, val)
                        elif best_play[1] < val:
                            best_play = (pos_key, val)
                        # print(f"POS {pos} VAL {val}")

        # print(f"Plays : {plays} Best Move : {best_play}")
        return best_play[0]


class Game:
    def __init__(self, attacking):

        self.board = Board()

        self.player = Player(not attacking)

        self.available_moves = {}

        self.set_available_moves()

        self.player_moves = set()

        self.ai_moves = set()

        self.value_dict = {"X": 10, "tie": 5, "O": -10}
        self.ai_attacking = attacking

        self.AI = AI(
            self.board,
            self.value_dict,
            self.board.len,
            self.ai_attacking,
        )

    def start(self):

        move = (3, 3)

        if self.ai_attacking:
            global move_count
            global ai_count
            self.set_move(move, "X")
            self.AI.set_move(self.available_moves[move], move)
            move_count += 1
            ai_count += 1
            self.available_moves = self.board.play(
                move, "X", self.available_moves, self.AI.get_moves(), {}
            )
            eval_board = self.board.get_evaluated_board()
            return {
                "won": False,
                "symbol": "-",
                "eval_board": eval_board,
            }
        else:
            eval_board = self.board.get_evaluated_board()
            return {
                "won": False,
                "symbol": "-",
                "eval_board": eval_board,
            }

    def remove_move(self, move):

        del self.available_moves[move]

    def set_available_moves(self):

        for i in range(self.board.len):

            for j in range(self.board.len):

                self.available_moves[(i, j)] = Move((i, j), "-")

                if i != 0:
                    self.available_moves[(i, j)].set_pos((i - 1, j), "up")

                if i + 1 != self.board.len:
                    self.available_moves[(i, j)].set_pos((i + 1, j), "down")

                if j != 0:
                    self.available_moves[(i, j)].set_pos((i, j - 1), "left")

                if j + 1 < self.board.len:

                    self.available_moves[(i, j)].set_pos((i, j + 1), "right")

                if i != 0 and j != 0:
                    self.available_moves[(i, j)].set_pos((i - 1, j - 1), "upleft")

                if i != 0 and j + 1 < self.board.len:
                    self.available_moves[(i, j)].set_pos((i - 1, j + 1), "upright")

                if i + 1 != self.board.len and j != 0:
                    self.available_moves[(i, j)].set_pos((i + 1, j - 1), "downleft")

                if i + 1 != self.board.len and j + 1 < self.board.len:
                    self.available_moves[(i, j)].set_pos((i + 1, j + 1), "downright")

    def set_move(self, pos, symbol):

        self.available_moves[pos].set_symbol(symbol)

    def get_symbol(self, pos):

        return self.available_moves[pos].get_symbol()

    def equals(self, item):

        last_index = 0
        symbol = None
        count = 0

        for index in range(len(item)):

            if count == 4:
                break

            if item[index] != "-":
                if symbol != item[index]:
                    symbol = item[index]
                    last_index = index
                    count = 1
                elif index == last_index + 1:
                    count += 1
                    last_index = index

        return (True, symbol) if count >= 4 else (False, symbol)

    def winner(self, board):

        global move_count

        for i in range(self.board.len):

            horizontal = self.board.get_board_arr((i, 0), "horizontal")
            won = self.equals(horizontal)

            if won[0]:

                print("horizontal win")
                if won[1] == "X":
                    return "X"
                elif won[1] == "O":
                    return "O"

            vertical = self.board.get_board_arr((0, i), "vertical")

            won = self.equals(vertical)

            if won[0]:

                print("vertical win")
                print(vertical)
                if won[1] == "X":
                    return "X"
                elif won[1] == "O":
                    return "O"

        for i in range(self.board.len):
            for j in range(self.board.len):
                diagonal_right = self.board.get_board_arr((i, j), "diagonal_right")
                won = self.equals(diagonal_right)

                if won[0]:

                    print("diagonal_right win")
                    print(diagonal_right)
                    if won[1] == "X":
                        return "X"
                    elif won[1] == "O":
                        return "O"

                diagonal_left = self.board.get_board_arr((i, j), "diagonal_left")

                won = self.equals(diagonal_left)

                if won[0]:

                    print("diagonal_left win")
                    print(diagonal_left)
                    if won[1] == "X":
                        return "X"
                    elif won[1] == "O":
                        return "O"

        # continue
        if move_count != 78:
            return "continue"

        # tie
        return "tie"

    def play(self, play, turn):

        global move_count
        global player_count
        global ai_count

        if turn == "player":
            player_count += 1
            move_count += 1
            self.set_move(play, "O")
            self.player.set_move(self.available_moves[play], play)
            self.available_moves = self.board.play(
                play,
                "O",
                self.available_moves,
                self.AI.get_moves(),
                self.player.get_moves(),
            )

            won = self.winner(self.board.board)

            eval_board = self.board.get_evaluated_board()

            if won == "O":
                print("YOU WON")
                return {
                    "won": True,
                    "symbol": "O",
                    "eval_board": eval_board,
                }

            elif won == "X":
                return {
                    "won": True,
                    "symbol": "X",
                    "eval_board": eval_board,
                }

            elif won == "tie":
                return {
                    "won": True,
                    "symbol": "-",
                    "eval_board": eval_board,
                }

        else:

            ai_count += 1
            move_count += 1
            move = self.AI.play(
                self.board,
                self.available_moves,
                self.player.get_moves(),
            )
            self.set_move(move, "X")
            self.AI.set_move(self.available_moves[move], move)
            self.available_moves = self.board.play(
                move,
                "X",
                self.available_moves,
                self.AI.get_moves(),
                self.player.get_moves(),
            )

            won = self.winner(self.board.board)

            eval_board = self.board.get_evaluated_board()

            # print("After my Move-")
            # self.board.print_board_state()
            # print("")

            if won == "O":
                print("YOU WON")
                return {
                    "won": True,
                    "symbol": "O",
                    "eval_board": eval_board,
                }

            elif won == "X":
                return {
                    "won": True,
                    "symbol": "X",
                    "eval_board": eval_board,
                }

            elif won == "tie":
                return {
                    "won": True,
                    "symbol": "-",
                    "eval_board": eval_board,
                }

        return {
            "won": False,
            "symbol": "-",
            "eval_board": eval_board,
        }
