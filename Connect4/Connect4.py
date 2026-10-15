from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax


class Connect4(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        self.field = " "
        self.board = []
        self.tokens = ["@", "O"]
        self.nplayer = 1
                
    def build(self):
        self.board = [self.field for i in range(42)]

    def possible_moves(self):
        return ["1", "2", "3", "4", "5", "6", "7"]

    def show(self):
        for idx, field in enumerate(self.board, start=1):
            print(f"[{field}]", end="")
            if idx % 7 == 0:
                print()
                
    def token(self):
        return self.tokens[self.nplayer - 1]

    def drop_token(self, column):
        for pos in range(35 + column - 1, -1, -7):
            if self.board[pos] == " ":
                self.board[pos] = self.token()
                return True
        return False

    def check_connect_x(self):
        count = 0
        for idx, field in enumerate(self.board, start=1):
            if field == self.token():
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            if idx % 7 == 0:
                count = 0
        return False

    def check_connect_y(self):
        count = 0
        for column in range(7):
            for pos in range(column, 42, 7):
                if self.board[pos] == self.token():
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
            count = 0
        return False

    def check_connect_z(self):

        r_step = 8
        l_step = 6
        matches = False
        
        for row in range(3):
            for col in range(7):
                idx = row * 7 + col
                if self.board[idx] == self.token() and col <= 3:
                    matches = [
                        self.board[idx + r_step] == self.token(),
                        self.board[idx + 2 * r_step] == self.token(),
                        self.board[idx + 3 * r_step] == self.token(),
                    ]
                    
                    if all(matches):
                        return True
                
                if self.board[idx] == self.token() and col >= 3:
                    matches = [
                        self.board[idx + l_step] == self.token(),
                        self.board[idx + 2 * l_step] == self.token(),
                        self.board[idx + 3 * l_step] == self.token(),
                    ]
                
                    if all(matches):
                        return True
        
        return False
        
    def make_move(self, move):
        return super().make_move(move)
    
    def clear_field(self, idx):
        self.board[idx] = " "

    def fill_field(self, idx):
        self.board[idx] = "@"
