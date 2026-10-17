"""Connect4 - gra "Cztery w rzędzie" dla dwóch graczy (człowiek vs człowiek lub człowiek vs AI).

Zasady gry:
    https://pl.wikipedia.org/wiki/Czw%C3%B3rka_w_rz%C4%99dzie
    (angielska wersja: https://en.wikipedia.org/wiki/Connect_Four)

    Plansza ma 6 wierszy i 7 kolumn. Gracze na zmianę wrzucają token do wybranej
    kolumny; token spada na najniższe wolne pole. Wygrywa ten, kto pierwszy ułoży
    cztery własne tokeny obok siebie w poziomie, w pionie lub po skosie.
    Jeśli plansza zapełni się bez zwycięzcy, jest remis.

Autorzy:
    - Jakub Kolad (s29741)
    - Igor Czeczot (s36735)

Przygotowanie środowiska:
    1. Zainstaluj Pythona 3.10 lub nowszego (https://www.python.org/downloads/).
    2. (Opcjonalnie) utwórz i aktywuj wirtualne środowisko:
           python -m venv venv
           venv\\Scripts\\activate        (Windows)
           source venv/bin/activate      (Linux / macOS)
    3. Zainstaluj bibliotekę easyAI (https://github.com/Zulko/easyAI):
           pip install easyAI
       Uwaga: w niektórych wersjach paczki z PyPI brakuje podpakietu easyAI.AI
       (błąd "No module named 'easyAI.AI'"). Wtedy:
           git clone https://github.com/Zulko/easyAI.git easyAI_repo
       i skopiuj folder easyAI_repo/easyAI (ten z plikiem __init__.py) obok
       tego pliku, tak aby powstał układ: Connect4.py + easyAI/__init__.py.
    4. Uruchom grę:
           python Connect4.py

Sterowanie:
    Gracz podaje numer kolumny (1-7). Domyślnie gra człowiek (@) kontra AI (O)
    z algorytmem Negamax o głębokości 4. W bloku __main__ można zamienić
    AI_Player na Human_Player, aby grać we dwie osoby.
"""

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax


class Connect4(TwoPlayerGame):
    """Gra Connect4 oparta na klasie TwoPlayerGame z biblioteki easyAI.

    Plansza jest przechowywana jako płaska lista 42 pól (6 wierszy x 7 kolumn),
    indeksowana wierszami od lewego górnego rogu: pole (wiersz, kolumna) ma
    indeks wiersz * 7 + kolumna. Ruch to numer kolumny (1-7).

    Attributes:
        players (list): lista dwóch graczy (Human_Player / AI_Player).
        field (str): znak oznaczający puste pole.
        board (list): płaska lista 42 pól planszy.
        tokens (list): znaki graczy; tokens[0] dla gracza 1, tokens[1] dla gracza 2.
        current_player (int): numer gracza na ruchu (1 lub 2).
        moves (list): wszystkie numery kolumn, w kolejności rozważania przez AI.
    """

    def __init__(self, players):
        """Inicjalizuje grę (plansza jest tworzona osobno metodą build).

        Parameters:
        players (list): lista dwóch obiektów graczy

        Returns:
        None
        """
        self.players = players
        self.field = " "
        self.board = []
        self.tokens = ["@", "O"]
        self.current_player = 1

        self.moves = [1, 2, 3, 4, 5, 6, 7]

    def build(self):
        """Tworzy pustą planszę 6x7 (42 pola wypełnione znakiem pustego pola).

        Returns:
        None
        """
        self.board = [self.field for i in range(42)]

    def possible_moves(self):
        """Zwraca listę dozwolonych ruchów, czyli kolumn, które nie są pełne.

        Returns:
        list: numery kolumn (int, 1-7), do których można jeszcze wrzucić token
        """
        return [col for col in self.moves if not self.check_column_full(col)]

    def show(self):
        """Wypisuje planszę w konsoli, wiersz po wierszu.

        Returns:
        None
        """
        for idx, field in enumerate(self.board, start=1):
            print(f"[{field}]", end="")
            if idx % 7 == 0:
                print()

    def token(self):
        """Zwraca token gracza, który jest teraz na ruchu.

        Returns:
        str: znak gracza na ruchu ('@' lub 'O')
        """
        return self.tokens[self.current_player - 1]

    def previous_token(self):
        """Zwraca token gracza, który wykonał ostatni ruch (przeciwnika gracza na ruchu).

        Metoda jest używana w is_over i scoring, ponieważ easyAI przełącza gracza
        po wykonaniu ruchu, a dopiero potem sprawdza koniec gry.

        Returns:
        str: znak gracza, który zagrał jako ostatni
        """
        return self.tokens[self.opponent_index - 1]

    def drop_token(self, column):
        """Wrzuca token gracza na ruchu do wskazanej kolumny.

        Token zajmuje najniższe wolne pole w kolumnie.

        Parameters:
        column (int): numer kolumny (1-7)

        Returns:
        bool: True, jeśli token został umieszczony; False, gdy kolumna jest
        poza zakresem lub pełna
        """
        if column < 1 or column > 7:
            return False
        for pos in range(35 + column - 1, -1, -7):
            if self.board[pos] == " ":
                self.board[pos] = self.token()
                return True
        return False

    def check_column_full(self, column):
        """Sprawdza, czy kolumna jest całkowicie zapełniona.

        Parameters:
        column (int): numer kolumny (1-7)

        Returns:
        bool: True, jeśli w kolumnie nie ma wolnego pola
        """
        for pos in range(column - 1, 42, 7):
            if self.board[pos] == " ":
                return False
        return True

    def check_connect_x(self, token):
        """Sprawdza, czy podany token tworzy cztery pola w poziomie.

        Licznik jest zerowany po każdym innym polu oraz na końcu każdego wiersza,
        dzięki czemu ciąg nie "zawija się" na następny wiersz.

        Parameters:
        token (str): sprawdzany znak gracza

        Returns:
        bool: True, jeśli istnieje poziomy ciąg czterech tokenów
        """
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
        """Sprawdza, czy podany token tworzy cztery pola w pionie.

        Parameters:
        token (str): sprawdzany znak gracza

        Returns:
        bool: True, jeśli istnieje pionowy ciąg czterech tokenów
        """
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
        """Sprawdza, czy podany token tworzy cztery pola po skosie (oba kierunki).

        Sprawdzane są tylko pola startowe w wierszach 0-2, z których czwórka
        mieści się na planszy:
            - w prawo-dół (krok 8): kolumny startowe 0-3,
            - w lewo-dół (krok 6): kolumny startowe 3-6.

        Parameters:
        token (str): sprawdzany znak gracza

        Returns:
        bool: True, jeśli istnieje ukośny ciąg czterech tokenów
        """
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
        """Sprawdza, czy plansza jest całkowicie zapełniona.

        Returns:
        bool: True, jeśli nie ma już wolnych pól
        """
        return all(field != " " for field in self.board)

    def is_over(self):
        """Sprawdza, czy gra się zakończyła (czwórka ostatniego gracza lub pełna plansza).

        Metoda wymagana przez easyAI; wywoływana bez argumentów.

        Returns:
        bool: True, jeśli gra jest zakończona
        """
        return self.has_four(self.previous_token()) or self.check_full()

    def scoring(self):
        """Ocenia pozycję z perspektywy gracza na ruchu (używane przez Negamax).

        Returns:
        int: -100, jeśli gracz na ruchu przegrał (przeciwnik ma czwórkę);
        0 w przypadku remisu lub pozycji nierozstrzygniętej
        """
        if self.has_four(self.previous_token()):
            return -100  # gracz na ruchu właśnie przegrał
        return 0  # remis albo pozycja nierozstrzygnięta

    def has_four(self, token):
        """Sprawdza, czy podany token ma cztery w rzędzie w dowolnym kierunku.

        Parameters:
        token (str): sprawdzany znak gracza

        Returns:
        bool: True, jeśli znaleziono czwórkę poziomo, pionowo lub po skosie
        """
        return (
            self.check_connect_x(token)
            or self.check_connect_y(token)
            or self.check_connect_z(token)
        )

    def make_move(self, move):
        """Wykonuje ruch gracza na ruchu (przełączanie gracza robi easyAI).

        Parameters:
        move (int): numer kolumny (1-7)

        Returns:
        None

        Raises:
        ValueError: gdy ruch jest niedozwolony (kolumna pełna lub poza zakresem)
        """
        if not self.drop_token(move):
            raise ValueError(f"Invalid move: {move}")

    def unmake_move(self, move):
        """Cofa ruch w danej kolumnie, zdejmując jej najwyższy token.

        Przyspiesza algorytm Negamax, bo nie trzeba kopiować całej gry.

        Parameters:
        move (int): numer kolumny (1-7), z której ruch jest cofany

        Returns:
        None
        """
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
