from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax


class Connect4(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        self.field = " "
        self.board = []
        self.tokens = ["@", "O"]
        self.current_player = 1

        self.moves = [1, 2, 3, 4, 5, 6, 7]

    def build(self):
        self.board = [self.field for i in range(42)]

    def possible_moves(self):
        return [col for col in self.moves if not self.check_column_full(col)]

    def show(self):
        for idx, field in enumerate(self.board, start=1):
            print(f"[{field}]", end="")
            if idx % 7 == 0:
                print()

    def token(self):
        return self.tokens[self.current_player - 1]

    def previous_token(self):
        return self.tokens[self.opponent_index - 1]

    def drop_token(self, column):
        if column < 1 or column > 7:
            return False
        for pos in range(35 + column - 1, -1, -7):
            if self.board[pos] == " ":
                self.board[pos] = self.token()
                return True
        return False

    def check_column_full(self, column):
        for pos in range(column - 1, 42, 7):
            if self.board[pos] == " ":
                return False
        return True

    def check_connect_x(self, token):
        count = 0
        for idx, field in enumerate(self.board, start=1):
            if field == token:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            if idx % 7 == 0:
                count = 0
        return False

    def check_connect_y(self, token):
        count = 0
        for column in range(7):
            for pos in range(column, 42, 7):
                if self.board[pos] == token:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
            count = 0
        return False

    def check_connect_z(self, token):

        r_step = 8
        l_step = 6

        for row in range(3):
            for col in range(7):
                idx = row * 7 + col
                if self.board[idx] == token and col <= 3:
                    matches = [
                        self.board[idx + r_step] == token,
                        self.board[idx + 2 * r_step] == token,
                        self.board[idx + 3 * r_step] == token,
                    ]

                    if all(matches):
                        return True

                if self.board[idx] == token and col >= 3:
                    matches = [
                        self.board[idx + l_step] == token,
                        self.board[idx + 2 * l_step] == token,
                        self.board[idx + 3 * l_step] == token,
                    ]

                    if all(matches):
                        return True

        return False

    def check_full(self):
        return all(field != " " for field in self.board)

    def is_over(self):
        return self.has_four(self.previous_token()) or self.check_full()

    def scoring(self):
        if self.has_four(self.previous_token()):
            return -100  # gracz na ruchu właśnie przegrał
        return 0  # remis albo pozycja nierozstrzygnięta

    def has_four(self, token):
        return (
            self.check_connect_x(token)
            or self.check_connect_y(token)
            or self.check_connect_z(token)
        )

    def make_move(self, move):
        if not self.drop_token(move):
            raise ValueError(f"Invalid move: {move}")

    def unmake_move(self, move):
        for pos in range(move - 1, 42, 7):
            if self.board[pos] != " ":
                self.board[pos] = " "
                return

    # def clear_field(self, idx):
    #     self.board[idx] = " "

    # def fill_field(self, idx):
    #     self.board[idx] = "@"


if __name__ == "__main__":
    # players = [Human_Player(), Human_Player()]
    players = [Human_Player(), AI_Player(Negamax(4))]
    game = Connect4(players)
    game.build()
    game.play()
    if game.has_four(game.previous_token()):
        print(f"Wygrał gracz {game.opponent_index}")
    else:
        print("Remis")
