from random import randint


class BoardException(Exception):
    pass


class BoardWrongShipException(BoardException):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Координаты не принадлежат доске"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class Dot:  # Класс описывающий точку с параметрами координат х и у
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # Магический метод сравнения, потребуется для проверки нахождения точки в определенном
        # условии(например сравнение координаты корабля и координаты выстрела)
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # Магический метод для отображения информации об объекте (не __str__, тк __repr__ выводит более
        # удобное (не просто вывод объекта, а вместе с параметрами(координатами точек)) отображение во время отладки(
        # например проверки работоспособности одного из классов)
        return f"({self.x},{self.y})"


class Ship:  # Класс описания корабля с параметрами:
    def __init__(self, head_dot, length, direction):
        self.head_dot = head_dot  # координаты носа корабля
        self.length = length  # длина корабля
        self.direction = direction  # направление расположения на игровом поле (вертикально или горизонтально)
        self.hp = length  # кол-во жизней равно длине корабля

    @property
    def dots(self):  # Метод для вывода списка точек корабля
        dots_list = []
        for i in range(self.length):
            cur_x = self.head_dot.x
            cur_y = self.head_dot.y
            if self.direction == 0:  # условие горизонтального расположения
                cur_y += i
            if self.direction == 1:  # вертикального
                cur_x += i
            dots_list.append(Dot(cur_x, cur_y))
        return dots_list

    def hit(self, shot):  # Метод проверки попадания (через __eq__)
        return shot in self.dots


class Board:  # Класс описания игровой доски с параметрами:
    def __init__(self, hidden=False, size=6):
        self.hidden = hidden  # Видимость доски
        self.size = size  # Ее размер
        self.field = [["·"] * size for i in range(size)]  # Пустое поле-шаблон
        self.list_of_ships = []  # Список кораблей
        self.count_of_hit_ships = 0  # Количество подбитых кораблей
        self.list_of_used_dots = []  # Список занятых точек

    def __str__(self):  # Метод для вывода стартовой доски
        start_field = ""
        start_field += "    1   2   3   4   5   6 "
        for i, j in enumerate(self.field):
            start_field += f"\n{i + 1}   " + "   ".join(j) + "  "

        if self.hidden:  # Условие замены видимости кораблей (в зависимости от хода компьютера или игрока)
            start_field = start_field.replace("■", "·")
        return start_field

    def out(self, turn):  # Проверка принадлежности координат игровому полю
        return not ((0 <= turn.x < self.size) and (0 <= turn.y < self.size))

    def contour(self, ship, verb=False):  # Метод для проверки радиуса в одну клетку от корабля при расстановке
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for i in ship.dots:
            for ix, iy in near:
                cur = Dot(i.x + ix, i.y + iy)
                if not (self.out(cur)) and cur not in self.list_of_used_dots:  # условие вывода обводки уничтоженного
                    # корабля
                    if verb:
                        self.field[cur.x][cur.y] = "T"
                    self.list_of_used_dots.append(cur)

    def add_ship(self, ship):  # Метод для расстановки кораблей
        for i in ship.dots:
            if self.out(i) or i in self.list_of_used_dots:  # Условие вывода исключения (при несоблюдении промежутка
                # для координат или использовании занятой точки)
                raise BoardWrongShipException()
        for i in ship.dots:
            self.field[i.x][i.y] = "■"
            self.list_of_used_dots.append(i)
        self.list_of_ships.append(ship)
        self.contour(ship)

    def shot(self, turn):  # Метод для проверки и совершения выстрела
        if self.out(turn):
            raise BoardOutException()
        if turn in self.list_of_used_dots:
            raise BoardUsedException()
        self.list_of_used_dots.append(turn)
        for ship in self.list_of_ships:
            if turn in ship.dots:
                ship.hp -= 1
                self.field[turn.x][turn.y] = "X"
                if ship.hp == 0:
                    self.count_of_hit_ships += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True
        self.field[turn.x][turn.y] = "T"
        print("Мимо!")
        return False

    def begin(self):  # После расстановки кораблей, очищаем список занятых точек
        self.list_of_used_dots = []


class Player:  # Класс для описания игроков
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):  # Метод хода с бесконечным циклом и отловом исключений
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):  # Класс описывающий случайных ход компьютера
    def ask(self):
        turn = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {turn.x + 1} {turn.y + 1}")
        return turn


class User(Player):  # Класс описывающий запрос координат ходов у пользователя
    def ask(self):
        while True:
            cords = input("Введите координаты: ").split()
            if len(cords) != 2:
                print("Введите 2 координаты")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


def greet():
    print(f"""
               Приветствую в игре Морской Бой.
               Последовательно вводите координаты хода через пробел в формате
               х - номер строки
               y - номер столбца
               Текущий Счет: Компьютер {PC_WINS} - {USER_WINS} Вы
    """)


class Game:  # Класс описывающий ход игры
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        pc = self.random_board()
        pc.hidden = True
        self.ai = AI(pc, player)
        self.user = User(player, pc)

    def random_board(self):  # Метод для создания случайной доски
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):  # Метод для случайного размещения кораблей
        all_ships = [1, 1, 1, 1, 2, 2, 3]
        board = Board(size=self.size)
        attempts = 0
        for length in all_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def loop(self):
        count = 0
        global PC_WINS
        global USER_WINS
        while True:
            print("Ваша доска:")
            print(self.user.board)
            print("Доска компьютера:")
            print(self.ai.board)
            if count % 2 == 0:
                print("Ваш ход")
                repeat = self.user.move()
            else:
                print("Ходит компьютер")
                repeat = self.ai.move()
            if repeat:
                count -= 1
            if self.ai.board.count_of_hit_ships == 7:
                print("Вы победили!")
                USER_WINS += 1
                break
            if self.user.board.count_of_hit_ships == 7:
                print("Победил компьютер!")
                PC_WINS += 1
                break
            count += 1

    def start(self):
        greet()
        self.loop()


PC_WINS = 0
USER_WINS = 0
while True:
    g = Game()
    g.start()
    answer = str(input('Хотите сыграть еще раз? Y - да, ENTER - выход: '))
    if answer.lower() == 'y' and 'Y':
        continue
    else:
        break
