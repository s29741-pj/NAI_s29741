class Board:
    def __init__(self):
        self.field = " "
        self.board = []
        # self.tokens = ["@", "O"]
        self.token = "@"

    def build(self):
        self.board = [self.field for i in range(42)]

    def show(self):
        for idx, field in enumerate(self.board, start=1):
            print(f"[{field}]", end="")
            if idx % 7 == 0:
                print()

    def drop_token(self, column):
        for pos in range(35 + column - 1, -1, -7):
            if self.board[pos] == " ":
                self.board[pos] = self.token
                return True
        return False

    def check_connect_x(self):
        count = 0
        for idx, field in enumerate(self.board, start=1):
            if field == self.token:
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
                if self.board[pos] == self.token:
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
            for col in range(6):
                idx = row * 7 + col
                if self.board[idx] == self.token and col <= 3:
                    matches = [
                        self.board[idx + r_step] == self.token,
                        self.board[idx + 2 * r_step] == self.token,
                        self.board[idx + 3 * r_step] == self.token,
                    ]
                    
                    if all(matches):
                        return True
                
                if self.board[idx] == self.token and col >= 3:
                    matches = [
                        self.board[idx + l_step] == self.token,
                        self.board[idx + 2 * l_step] == self.token,
                        self.board[idx + 3 * l_step] == self.token,
                    ]
                
                    if all(matches):
                        return True
        
        return False
        
        # l_step = 6
        # for row in range(3):
        #     for col in range(3, 7):
        #         idx = row * 7 + col
        #         if self.board[idx] == self.token:
        #             matches = [
        #                 self.board[idx + l_step] == self.token,
        #                 self.board[idx + 2 * l_step] == self.token,
        #                 self.board[idx + 3 * l_step] == self.token,
        #             ]
        #             if all(matches):
        #                 return True



    def clear_field(self, idx):
        self.board[idx] = " "

    def fill_field(self, idx):
        self.board[idx] = "@"


def main():
    board = Board()
    board.build()

    # board.drop_token(1)
    # board.drop_token(1)
    # board.drop_token(1)
    # board.drop_token(1)
    # board.drop_token(1)
    # board.drop_token(1)

    # board.drop_token(2)
    # board.drop_token(2)
    # board.drop_token(2)
    # board.drop_token(2)
    # board.drop_token(2)

    # board.drop_token(3)
    # board.drop_token(3)
    # board.drop_token(3)
    # board.drop_token(3)

    # board.drop_token(4)
    # board.drop_token(4)
    # board.drop_token(4)

    # board.fill_field(0)
    # board.fill_field(8)
    # board.fill_field(16)
    # board.fill_field(24)

    # board.fill_field(3)
    # board.fill_field(9)
    # board.fill_field(15)
    # board.fill_field(21)

    board.fill_field(3)
    board.fill_field(11)
    board.fill_field(19)
    # board.fill_field(27)
    
    
    # board.fill_field(3)
    # board.fill_field(9)
    # board.fill_field(15)
    # board.fill_field(21)
    board.fill_field(35)

    # board.fill_field(35)
    # board.fill_field(28)
    # board.fill_field(1)
    # board.fill_field(8)

    # board.clear_field(41)
    # board.clear_field(40)
    print("X", board.check_connect_x())
    print("Y", board.check_connect_y())
    print("Z", board.check_connect_z())
    board.show()


if __name__ == "__main__":
    main()
