def matrix_final(matrix):  # функция для записи ходов в начальную матрицу
    print('   1  2  3')
    for i in range(3):
        print(i + 1, *matrix[i])


def turns():  # функция хода игры(получение значений и проверка возможности хода, проверка значения хода)
    while True:
        i = input("Введите номер строки: ")
        j = input("Введите номер столбца: ")
        if not (i.isdigit()) or not (j.isdigit()):
            print("Ошибка ввода, введите число")
            continue
        i, j = int(i), int(j)
        if i < 1 or j < 1 or i > 3 or j > 3:
            print("Ошибка ввода, число не принадлежит интервалу")
            continue
        if draft_matrix[i - 1][j - 1] != ' -':
            print("Клетка уже была использована")
            continue
        return i, j


def win_cond():  # условие победы одного из игроков (любая из строк или столбцов, две диагонали матрицы), проверка и
    # определение победителя
    win_condition = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                     ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                     ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for win in win_condition:
        turn = []
        for w in win:
            turn.append(draft_matrix[w[0]][w[1]])
        if turn == [' x', ' x', ' x']:
            print("Игрок Крестики победил!")
            return True
        if turn == [' o', ' o', ' o']:
            print("Игрок Нолики победил!")
            return True
    return False


def restart():  # функция перезапуска игры по желанию
    print("Хотите начать заново?")
    answer = str(input("Введите ответ: Y - начать заново, ENTER - выйти из игры \n"))
    if answer.lower() == "y":
        return True
    else:
        return False


while True:  # цикл самой игры
    draft_matrix = [[' -'] * 3 for i in range(3)]  # создание пустой матрицы для последуйщей записи ходов
    count = 0  # счетчик определения игрока (четные - нолики, нечетные - крестики)
    while True:
        matrix_final(draft_matrix)
        count += 1
        if count % 2 == 1:
            print("Ход игрока Крестики")
        else:
            print("Ход игрока Нолики")
        i, j = turns()
        if count % 2 == 1:
            draft_matrix[i - 1][j - 1] = ' x'
        else:
            draft_matrix[i - 1][j - 1] = ' o'
        if count == 9:
            print("Ничья!")
            matrix_final(draft_matrix)
            break
        if win_cond():
            matrix_final(draft_matrix)
            break
    if restart():
        continue
    else:
        break
