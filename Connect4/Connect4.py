from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax


class Connect4(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        self.field = " "
        self.board = [field for field in self.board if len(self.board) < 42]
        self.tokens = ["@", "O"]
        self.nplayer = 1

    def possible_moves(self):
        return ["1", "2", "3", "4", "5", "6", "7"]

    # def drop_token(players, tokens):

    # def check_connect(board,tokens):

    def make_move(self, move):
        return super().make_move(move)
