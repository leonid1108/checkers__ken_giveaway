import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *

ws = Tk()
ws.title("Кены-поддавки")

WIDTH, HEIGHT = 1200, 800
canvas = Canvas(ws, width=WIDTH, height=HEIGHT)
canvas.pack()

# Возможность ходить
abilGoWalkWhite, abilGoWalkBlack = False, False

# Количество шашек, переменные для статистики, кол-во ходов для алгоритма ничьей
number_of_whites, number_of_blacks = 16, 16
win_white, win_black = 0, 0
numberMovesDraw = 0
checkingProgress = False

past_value_white_x, past_value_white_y = 0, 0
past_value_black_x, past_value_black_y = 0, 0

# Для перепрыгивания через союзника
skippingFriend = False
skippingFriendSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}

# Воз-ть белых ходить
capWhiteCollect = False
capWhiteCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}
# Воз-ть белых дамок ходить
capWhiteDamCollect = False
capWhiteDamCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}
# Воз-ть чёрных ходить
capBlackCollect = False
capBlackCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}
# Воз-ть чёрных дамок ходить
capBlackDamCollect = False
capBlackDamCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}

black_che = PhotoImage(file='src/black_checkers.png')
white_che = PhotoImage(file='src/white_checkers.png')
white_dam = PhotoImage(file='src/white_checkers_king.png')
black_dam = PhotoImage(file='src/black_checkers_king.png')

checkers = [0, white_che, black_che, white_dam, black_dam]

def select_move():
    global move_of_white
    if askyesno("Выбор хода", "Ход за белыми?"):
        move_of_white = True
    else:
        move_of_white = False

def new_game():
    global board
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
             [2, 2, 2, 2, 0, 2, 2, 2],
             [2, 2, 2, 2, 1, 2, 2, 2],
             [0, 0, 0, 0, 2, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 0, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0]]


def start_new():
    global number_of_whites, number_of_blacks
    global numberMovesDraw, checkingProgress
    if askyesno("Игра окончена", "Хотите начать новую?"):
        new_game()
        select_move()
        draw_board(-1, -1)
        number_of_whites, number_of_blacks = 16, 16
        numberMovesDraw = 0
        checkingProgress = False


def checking_the_end():
    global number_of_whites, number_of_blacks
    global win_white, win_black
    global move_of_white
    draw_board(-1, -1)

    if number_of_whites == 0:
        messagebox.showinfo(title="White's Victory", message="Победили белые!", icon='info')
        move_of_white = True
        win_white += 1
        start_new()

    if number_of_blacks == 0:
        messagebox.showinfo(title="Black's victory", message="Победили чёрные!", icon="info")
        move_of_white = False
        win_black += 1
        start_new()

    if numberMovesDraw == 10 and checkingProgress == False:
        messagebox.showinfo(title="Draw!", message="Ничья!\nЗа 10 ходов не было ни одной жертвы!", icon="info")
        move_of_white = None
        start_new()

def draw_board(position_x_1, position_y_1):
    global checkers, board
    x = 0
    canvas.delete('all')
    canvas.create_rectangle(1200, 0, 800, 1000, fill="#505050")

    canvas.create_text(980, 125, fill="white", font="Open 18 bold", text=f"Количество белых шашек:\n{number_of_whites}")
    canvas.create_text(985, 225, fill="white", font="Open 18 bold", text=f"Количество чёрных шашек:\n{number_of_blacks}")

    canvas.create_text(1000, 400, fill="white", font="Open 16 bold", text="Белые || Чёрные")
    canvas.create_text(995, 425, fill="white", font="Open 16 bold", text=f"{win_white}:{win_black}")

    while x < 8 * 100:
        y = 100
        while y < 8 * 100:
            canvas.create_rectangle(x, y, x + 100, y + 100, fill="grey")
            y += 100
        x += 100
    x = 0
    while x < 8 * 100:
        y = 0
        while y < 8 * 100:
            canvas.create_rectangle(x, y, x + 100, y + 100, fill="grey")
            y += 100
        x += 100

    for y in range(8):
        for x in range(8):
            if board[y][x]:
                if (position_x_1, position_y_1) != (x, y):
                    canvas.create_image(x * 100, y * 100, anchor=NW, image=checkers[board[y][x]])


def possibility_walk(x, y, color):
    global abilGoWalkWhite, abilGoWalkBlack
    global past_value_white_x, past_value_white_y
    global past_value_black_x, past_value_black_y
    global move_of_white
    if color == 1:
        if board[x][y] == 1: # Для белой шашки
            if (board[x][y - 1] == 0 and y > 0) or (board[x - 1][y] == 0 and x > 0) or (y < 7 and board[x][y + 1] == 0):
                abilGoWalkWhite = True
            else:
                abilGoWalkWhite = False
            past_value_white_x = x
            past_value_white_y = y
        if board[x][y] == 3: # Для белой дамки
            if (x < 7 and board[x + 1][y] == 0) or (x > 0 and board[x - 1][y] == 0) or (
                    board[x][y - 1] == 0 and y > 0) or (
                    y < 7 and board[x][y + 1] == 0):
                abilGoWalkWhite = True
            else:
                abilGoWalkWhite = False
            past_value_white_x = x
            past_value_white_y = y

    elif color == 2:
        if board[x][y] == 2:  # Для чёрной шашки
            if (board[x + 1][y] == 0 and x < 7) or (y < 7 and board[x][y + 1] == 0) or (board[x][y - 1] == 0 and y > 0):
                abilGoWalkBlack = True
            else:
                abilGoWalkBlack = False
            past_value_black_x = x
            past_value_black_y = y
        if board[x][y] == 4:  # Для чёрной дамки
            if (x > 0 and board[x - 1][y] == 0) or (x < 7 and board[x + 1][y] == 0) or (
                    y < 7 and board[x][y + 1] == 0) or (
                    y > 0 and board[x][y - 1] == 0):
                abilGoWalkBlack = True
            else:
                abilGoWalkBlack = False
            past_value_black_x = x
            past_value_black_y = y

def checking_checkers(color):
    global skippingFriend, skippingFriendSides
    global capBlackCollect, capBlackCollectSides
    global capWhiteCollect, capWhiteCollectSides

    # Для белых
    if color == 1:
        for x in range(8):
            for y in range(8):
                if (board[x][y] == 1 and y > 1) and (board[x][y - 1] == 2 or board[x][y - 1] == 4) \
                        and board[x][y - 2] == 0:  # Для белой шашки влево
                    capWhiteCollect = True
                    capWhiteCollectSides["Left"] = True
                if (board[x][y] == 1 and x > 1) and (board[x - 1][y] == 2 or board[x - 1][y] == 4) \
                        and board[x - 2][y] == 0:  # Для белой шашки вверх
                    capWhiteCollect = True
                    capWhiteCollectSides["Up"] = True
                if (board[x][y] == 1 and y < 6) and (board[x][y + 1] == 2 or board[x][y + 1] == 4) \
                        and board[x][y + 2] == 0:  # Для белой шашки вправо
                    capWhiteCollect = True
                    capWhiteCollectSides["Right"] = True
                if (board[x][y] == 1 and x < 6) and (board[x + 1][y] == 2 or board[x + 1][y] == 4) \
                        and board[x + 2][y] == 0:  # Для белой шашки вниз
                    capWhiteCollect = True
                    capWhiteCollectSides["Down"] = True


                if (board[x][y] == 1 and y > 1) and (board[x][y - 1] == 1 or board[x][y - 1] == 3) \
                        and board[x][y - 2] == 0: # Для перепрыгивания белой шашки влево
                    skippingFriend = True
                    skippingFriendSides["Left"] = True
                if (board[x][y] == 1 and x > 1) and (board[x - 1][y] == 1 or board[x - 1][y] == 3) \
                        and board[x - 2][y] == 0: # Для перепрыгивания белой шашки вверх
                    skippingFriend = True
                    skippingFriendSides["Up"] = True
                if (board[x][y] == 1 and y < 6) and (board[x][y + 1] == 1 or board[x][y + 1] == 3) \
                        and board[x][y + 2] == 0: # Для перепрыгивания белой шашки вправо
                    skippingFriend = True
                    skippingFriendSides["Right"] = True


    # Для чёрных
    elif color == 2:
        for x in range(8):
            for y in range(8):
                if (board[x][y] == 2 and y > 1) and (board[x][y - 1] == 1 or board[x][y - 1] == 3) \
                        and board[x][y - 2] == 0: # Для чёрной шашки влево
                    capBlackCollectSides["Left"] = True
                    capBlackCollect = True
                if (board[x][y] == 2 and x > 1) and (board[x - 1][y] == 1 or board[x - 1][y] == 3) \
                        and board[x - 2][y] == 0: # Для чёрной шашки вверх
                    capBlackCollect = True
                    capBlackCollectSides["Up"] = True
                if (board[x][y] == 2 and y < 6) and (board[x][y + 1] == 1 or board[x][y + 1] == 3) \
                        and board[x][y + 2] == 0: # Для чёрной шашки вправо
                    capBlackCollect = True
                    capBlackCollectSides["Right"] = True
                if (board[x][y] == 2 and x < 6) and (board[x + 1][y] == 1 or board[x + 1][y] == 3) \
                        and board[x + 2][y] == 0: # Для чёрной шашки вниз
                    capBlackCollectSides["Down"] = True
                    capBlackCollect = True

                if (board[x][y] == 2 and y > 1) and (board[x][y - 1] == 2 or board[x][y - 1] == 4) \
                        and board[x][y - 2] == 0: # Для перепрыгивания чёрной шашки влево
                    skippingFriend = True
                    skippingFriendSides["Left"] = True
                if (board[x][y] == 2 and y < 6) and (board[x][y + 1] == 2 or board[x][y + 1] == 4) \
                        and board[x][y + 2] == 0:# Для перепрыгивания чёрной шашки вправо
                    skippingFriend = True
                    skippingFriendSides["Right"] = True
                if (board[x][y] == 2 and x < 6) and (board[x + 1][y] == 2 or board[x + 1][y] == 4) \
                        and board[x + 2][y] == 0: # Для перепрыгивания чёрной шашки вниз
                    skippingFriend = True
                    skippingFriendSides["Down"] = True

def checking_checkers_king(color):
    global capWhiteDamCollect, capWhiteDamCollectSides
    global capBlackDamCollect, capBlackDamCollectSides

    if color == 1:
        for x in range(8):
            for y in range(8):
                if board[x][y] == 3 and y > 1:
                    for index in range(8):
                        empty_cell, black_cell, count = 0, 0, 0
                        if board[x][index] == 0 and (
                                index < 6 and board[x][index + 2] == 0 or index < 6 and board[x][index + 2] == 3) and (
                                (index < 7 and board[x][index + 1] == 2) or (index < 7 and board[x][index + 1] == 4)):
                            while board[x][index] != 3:
                                if board[x][index + 1] == 3 and index < 7:
                                    capWhiteDamCollectSides["Left"] = True
                                    capWhiteDamCollect = True
                                    break
                                black_cell += 1
                                if index < 7:
                                    index += 1
                                else:
                                    break
                                if board[x][index] == 0:
                                    empty_cell += 1
                                if board[x][index] == 2 or board[x][index] == 4:
                                    count += 1
                                if count == 2:
                                    break
                                if empty_cell == black_cell - 2 and board[x][index] == 3:
                                    capWhiteDamCollectSides["Left"] = True
                                    capWhiteDamCollect = True
                                else:
                                    capWhiteDamCollectSides["Left"] = False
                if board[x][y] == 3 and x > 1:
                    for index in range(8):
                        empty_cell, black_cell, count = 0, 0, 0
                        if board[index][y] == 0 and (
                                (index < 7 and board[index + 1][y] == 2) or (
                                index < 7 and board[index + 1][y] == 4)) and (
                                index < 6 and board[index + 2][y] == 0 or index < 6 and board[index + 2][y] == 3):
                            while board[index][y] != 3:
                                if index < 7 and board[x][index + 1] == 3:
                                    capWhiteDamCollectSides["Up"] = True
                                    capWhiteDamCollect = True
                                    break
                                black_cell += 1
                                if index < 7:
                                    index += 1
                                else:
                                    break
                                if board[index][y] == 0:
                                    empty_cell += 1
                                if board[index][y] == 2 or board[index][y] == 4:
                                    count += 1
                                if count == 2:
                                    break
                                if empty_cell == black_cell - 2 and board[index][y] == 3:
                                    capWhiteDamCollectSides["Up"] = True
                                    capWhiteDamCollect = True
                                else:
                                    capWhiteDamCollectSides["Up"] = False
                if board[x][y] == 3 and y < 7:
                    for index in range(8):
                        empty_cell, black_cell = 0, 0
                        if board[x][index] == 0 and (
                                (index > 1 and board[x][index - 1] == 2) or (index > 1 and board[x][index - 1] == 4)):
                            while board[x][index] != 3:
                                black_cell += 1
                                index -= 1
                                if board[x][index] == 0:
                                    empty_cell += 1
                                if empty_cell == black_cell - 2 and board[x][index] == 3:
                                    capWhiteDamCollectSides["Right"] = True
                                    capWhiteDamCollect = True
                                else:
                                    capWhiteCollectSides["Right"] = False
                            break
                if board[x][y] == 3 and x < 7:
                    for index in range(8):
                        empty_cell, black_cell = 0, 0
                        if board[index][y] == 0 and (
                                (index > 1 and board[index - 1][y] == 2) or (index > 1 and board[index - 1][y] == 4)):
                            while board[index][y] != 3:
                                black_cell += 1
                                index -= 1
                                if board[index][y] == 0:
                                    empty_cell += 1
                                if empty_cell == black_cell - 2 and board[index][y] == 3:
                                    capWhiteDamCollectSides["Down"] = True
                                    capWhiteDamCollect = True
                                else:
                                    capWhiteDamCollectSides["Down"] = False
                            break

    elif color == 2:
        for x in range(8):
            for y in range(8):
                if y > 1 and board[x][y] == 4:
                    for index in range(8):
                        empty_cell, black_cell, count = 0, 0, 0
                        if board[x][index] == 0 and (
                                (index < 7 and board[x][index + 1] == 1) or (
                                index < 7 and board[x][index + 1] == 3)) and (
                                index < 6 and board[x][index + 2] == 0 or index < 6 and board[x][index + 2] == 4):
                            while board[x][index] != 4:

                                if index < 7 and board[x][index + 1] == 4:
                                    capBlackDamCollectSides["Left"] = True
                                    capBlackDamCollect = True
                                    break
                                black_cell += 1
                                if index < 7:
                                    index += 1
                                else:
                                    break

                                if board[x][index] == 0:
                                    empty_cell += 1
                                if board[x][index] == 1 or board[x][index] == 3:
                                    count += 1
                                if count == 2:
                                    break
                                if empty_cell == black_cell - 2 and board[x][index] == 4:
                                    capBlackDamCollectSides["Left"] = True
                                    capBlackDamCollect = True
                                else:
                                    capBlackDamCollectSides["Left"] = False
                if x > 1 and board[x][y] == 4:
                    for index in range(8):
                        empty_cell, black_cell, count = 0, 0, 0
                        if board[index][y] == 0 and (
                                (index < 7 and board[index + 1][y] == 1) or (
                                index < 7 and board[index + 1][y] == 3)) and (
                                index < 6 and board[index + 2][y] == 0 or index < 6 and board[index + 2][y] == 4):
                            while board[index][y] != 4:
                                if index < 7 and board[x][index + 1] == 4:
                                    capBlackDamCollectSides["Up"] = True
                                    capBlackDamCollect = True
                                    break
                                black_cell += 1
                                if index < 7:
                                    index += 1
                                else:
                                    break
                                if board[index][y] == 0:
                                    empty_cell += 1
                                if board[index][y] == 1 or board[index][y] == 3:
                                    count += 1
                                if count == 2:
                                    break
                                if empty_cell == black_cell - 2 and board[index][y] == 4:
                                    capBlackDamCollectSides["Up"] = True
                                    capBlackDamCollect = True
                                else:
                                    capBlackDamCollectSides["Up"] = False
                if y < 7 and board[x][y] == 4:
                    for index in range(8):
                        empty_cell, black_cell = 0, 0
                        if board[x][index] == 0 and (
                                (index > 1 and board[x][index - 1] == 1) or (index > 1 and board[x][index - 1] == 3)):
                            while board[x][index] != 4:

                                black_cell += 1
                                index -= 1

                                if board[x][index] == 0:
                                    empty_cell += 1
                                if empty_cell == black_cell - 2 and board[x][index] == 4:
                                    capBlackDamCollectSides["Right"] = True
                                    capBlackDamCollect = True
                                else:
                                    capBlackCollectSides["Right"] = False
                            break
                if x < 7 and board[x][y] == 4:
                    for index in range(8):
                        empty_cell, black_cell = 0, 0
                        if board[index][y] == 0 and (
                                (index > 1 and board[index - 1][y] == 1) or (index > 1 and board[index - 1][y] == 3)):
                            while board[index][y] != 4:
                                black_cell += 1
                                index -= 1
                                if board[index][y] == 0:
                                    empty_cell += 1
                                if empty_cell == black_cell - 2 and board[index][y] == 4:
                                    capBlackDamCollectSides["Down"] = True
                                    capBlackDamCollect = True
                                else:
                                    capBlackDamCollectSides["Down"] = False
                            break





def stroke_processing(event):
    global move_of_white, numberMovesDraw, checkingProgress
    global number_of_whites, number_of_blacks

    global capWhiteCollect, capWhiteCollectSides
    global capBlackCollect, capBlackCollectSides
    global capWhiteDamCollect, capWhiteDamCollectSides
    global capBlackDamCollect, capBlackDamCollectSides

    global past_value_white_x, past_value_white_y
    global past_value_black_x, past_value_black_y

    if checkingProgress == True:
        checkingProgress = False
        numberMovesDraw = 0

    if event.x < 800 and event.x > 0 and event.y < 800 and event.y > 0:
        x, y = event.y // 100, event.x // 100
        if move_of_white:
            if capWhiteDamCollect:
                if capWhiteDamCollectSides["Left"]:
                    if board[past_value_white_x][past_value_white_y] == 3 and past_value_white_y > 1 and \
                            board[x][y] == 0 and past_value_white_x == x:
                        if y < past_value_white_y and y < 7 and board[x][y + 1] == 2 or y < 7 and board[x][y + 1] == 4:
                            black_cell, not_empty_cell = 0, 0
                            old_y = past_value_white_y
                            for index in range(past_value_white_y, y, -1):
                                black_cell += 1
                                if board[x][past_value_white_y] != 0:
                                    not_empty_cell += 1
                                past_value_white_y -= 1
                            if not_empty_cell == 2:
                                board[x][y] = 3
                                board[past_value_white_x][old_y] = 0
                                board[x][y + 1] = 0
                                checkingProgress = True
                                number_of_blacks -= 1
                                draw_board(-1, -1)
                if capWhiteDamCollectSides["Up"]:
                    if board[past_value_white_x][past_value_white_y] == 3 and past_value_white_x > 1 and \
                            board[x][y] == 0 and past_value_white_y == y:
                        if x < past_value_white_x and x < 7 and board[x + 1][y] == 2 or x < 7 and board[x + 1][y] == 4:
                            black_cell, not_empty_cell = 0, 0
                            old_x = past_value_white_x
                            for index in range(past_value_white_x, x, -1):
                                black_cell += 1
                                if board[past_value_white_x][y] != 0:
                                    not_empty_cell += 1
                                past_value_white_x -= 1
                            if not_empty_cell == 2:
                                board[x][y] = 3
                                board[old_x][past_value_white_y] = 0
                                board[x + 1][y] = 0
                                checkingProgress = True
                                number_of_blacks -= 1
                                draw_board(-1, -1)
                if capWhiteDamCollectSides["Right"]:
                    if board[past_value_white_x][past_value_white_y] == 3 and past_value_white_y < 6 and \
                            board[x][y] == 0 and past_value_white_x == x:
                        if y > past_value_white_y and board[x][y - 1] == 2 or board[x][y - 1] == 4:
                            black_cell, not_empty_cell = 0, 0
                            old_y = past_value_white_y
                            for index in range(y, past_value_white_y, -1):
                                black_cell += 1
                                if board[x][past_value_white_y] != 0:
                                    not_empty_cell += 1
                                past_value_white_y += 1
                            if not_empty_cell == 2:
                                board[x][y] = 3
                                board[past_value_white_x][old_y] = 0
                                board[x][y - 1] = 0
                                checkingProgress = True
                                number_of_blacks -= 1
                                draw_board(-1, -1)
                if capWhiteDamCollectSides["Down"]:
                    if board[past_value_white_x][past_value_white_y] == 3 and past_value_white_x < 7 and \
                            board[x][y] == 0 and past_value_white_y == y:
                        if x > past_value_white_x and board[x - 1][y] == 2 or board[x - 1][y] == 4:
                            black_cell, not_empty_cell = 0, 0
                            old_x = past_value_white_x
                            for index in range(x, past_value_white_x, -1):
                                black_cell += 1
                                if board[past_value_white_x][y] != 0:
                                    not_empty_cell += 1
                                past_value_white_x += 1
                            if not_empty_cell == 2:
                                board[x][y] = 3
                                board[old_x][past_value_white_y] = 0
                                board[x - 1][y] = 0
                                checkingProgress = True
                                number_of_blacks -= 1
                                draw_board(-1, -1)
                capWhiteDamCollect = False
                checking_checkers(1)
                checking_checkers_king(1)
                if capWhiteDamCollect == False:
                    move_of_white = False

            if capWhiteCollect:
                if capWhiteCollectSides["Left"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_y > 1 and (
                            board[past_value_white_x][past_value_white_y - 1] == 2 or
                            board[past_value_white_x][past_value_white_y - 1] == 4) and board[x][y] == 0 and \
                            board[past_value_white_x][
                                past_value_white_y - 2] == 0 and past_value_white_x == x and past_value_white_y == y + 2:
                        board[past_value_white_x][y + 2] = 0
                        board[x][y + 1] = 0
                        board[x][y] = 1
                        checkingProgress = True
                        number_of_blacks -= 1
                        draw_board(-1, -1)
                if capWhiteCollectSides["Up"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_x > 1 and (
                            board[past_value_white_x - 1][y] == 2 or board[past_value_white_x - 1][y] == 4) and \
                            board[x][y] == 0 and board[x + 2][y] == 1 and past_value_white_x == x + 2 and past_value_white_y == y:
                        if past_value_white_x == 2 and x == 0:
                            board[x][y] = 3
                        else:
                            board[x][y] = 1
                        board[x + 2][y] = 0
                        board[x + 1][y] = 0
                        checkingProgress = True
                        number_of_blacks -= 1
                        draw_board(-1, -1)
                if capWhiteCollectSides["Right"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_y < 6 and (
                            board[past_value_white_x][past_value_white_y + 1] == 2 or
                            board[past_value_white_x][past_value_white_y + 1] == 4) and board[x][y] == 0 and \
                            board[past_value_white_x][
                                past_value_white_y + 2] == 0 and past_value_white_x == x and past_value_white_y == y - 2:
                        board[past_value_white_x][y - 2] = 0
                        board[x][y - 1] = 0
                        board[x][y] = 1
                        number_of_blacks -= 1
                        checkingProgress = True
                        draw_board(-1, -1)
                if capWhiteCollectSides["Down"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_x < 6 and (
                            board[past_value_white_x + 1][y] == 2 or board[past_value_white_x + 1][y] == 4) and \
                            board[x][y] == 0 and past_value_white_x == x - 2 and past_value_white_y == y:
                        board[x - 2][y] = 0
                        board[x - 1][y] = 0
                        board[x][y] = 1
                        checkingProgress = True
                        number_of_blacks -= 1
                        draw_board(-1, -1)
                capWhiteCollect = False
                checking_checkers(1)
                checking_checkers_king(1)
                if capWhiteDamCollect == False and capWhiteCollect == False:
                    move_of_white = False
            if skippingFriend:
                if skippingFriendSides["Left"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_y > 1 and (
                            board[past_value_white_x][past_value_white_y - 1] == 1 or
                            board[past_value_white_x][past_value_white_y - 1] == 3) and board[x][y] == 0 and \
                            board[past_value_white_x][
                                past_value_white_y - 2] == 0 and past_value_white_x == x and past_value_white_y == y + 2:
                        board[past_value_white_x][y + 2] = 0
                        board[x][y] = 1
                        draw_board(-1, -1)
                        move_of_white = False

                if skippingFriendSides["Up"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_x > 1 and \
                            (board[past_value_white_x - 1][y] == 1 or board[past_value_white_x - 1][y] == 3) \
                            and board[x][y] == 0 and board[x + 2][
                        y] == 1 and past_value_white_x == x + 2 and past_value_white_y == y:
                        if past_value_white_x == 2 and x == 0:
                            board[x][y] = 3
                        else:
                            board[x][y] = 1
                        board[x + 2][y] = 0
                        draw_board(-1, -1)
                        move_of_white = False

                if skippingFriendSides["Right"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_y < 6 and (
                            board[past_value_white_x][past_value_white_y + 1] == 1 or
                            board[past_value_white_x][past_value_white_y + 1] == 3) and board[x][y] == 0 and \
                            board[past_value_white_x][
                                past_value_white_y + 2] == 0 and past_value_white_x == x and past_value_white_y == y - 2:
                        board[past_value_white_x][y - 2] = 0
                        board[x][y] = 1
                        draw_board(-1, -1)
                        move_of_white = False
                checking_checkers(1)
                checking_checkers_king(1)
            checking_checkers(1)
            checking_checkers_king(1)
            possibility_walk(x, y, 1)
            checking_the_end()
            if abilGoWalkWhite:
                if (board[past_value_white_x][
                        past_value_white_y] != 0 and past_value_white_y + 1 == y and past_value_white_x == x) or (
                        past_value_white_y - 1 == y and past_value_white_x == x) or (
                        past_value_white_x - 1 == x and past_value_white_y == y):
                    if board[x][y] == 0 and capWhiteCollect == False and capWhiteDamCollect == False:
                        if board[past_value_white_x][
                            past_value_white_y] == 1:
                            if x == 0:
                                board[x][y] = 3
                            else:
                                board[x][y] = 1
                            board[past_value_white_x][past_value_white_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = False
                if board[past_value_white_x][past_value_white_y] == 3 and board[x][
                    y] == 0 and capWhiteCollect == False and capWhiteDamCollect == False:
                    if past_value_white_x > x and past_value_white_y == y:
                        black_cell, not_empty_cell = 0, 0
                        old_x = past_value_white_x
                        for index in range(past_value_white_x, x, -1):
                            black_cell += 1
                            if board[past_value_white_x][y] != 0:
                                not_empty_cell += 1
                            past_value_white_x -= 1
                        if not_empty_cell == 1:
                            board[x][y] = 3
                            board[old_x][past_value_white_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = False
                    if past_value_white_x < x and past_value_white_y == y:
                        black_cell, not_empty_cell = 0, 0
                        old_x = past_value_white_x
                        for index in range(past_value_white_x, x):
                            black_cell += 1
                            if board[past_value_white_x][y] != 0:
                                not_empty_cell += 1
                            past_value_white_x += 1
                        if not_empty_cell == 1:
                            board[x][y] = 3
                            board[old_x][past_value_white_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = False
                    if past_value_white_y > y and past_value_white_x == x:
                        black_cell, not_empty_cell = 0, 0
                        old_y = past_value_white_y
                        for index in range(past_value_white_y, y, -1):
                            black_cell += 1
                            if board[x][past_value_white_y] != 0:
                                not_empty_cell += 1
                            past_value_white_y -= 1
                        if not_empty_cell == 1:
                            board[x][y] = 3
                            board[past_value_white_x][old_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = False
                    if past_value_white_y < y and past_value_white_x == x:
                        black_cell, not_empty_cell = 0, 0
                        old_y = past_value_white_y
                        for index in range(past_value_white_y, y):
                            black_cell += 1
                            if board[x][past_value_white_y] != 0:
                                not_empty_cell += 1
                            past_value_white_y += 1
                        if not_empty_cell == 1:
                            board[x][y] = 3
                            board[past_value_white_x][old_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = False

        else:
            if capBlackDamCollect:
                if capBlackDamCollectSides["Left"]:
                    if board[past_value_black_x][past_value_black_y] == 4 and past_value_black_y > 1 and \
                            board[x][y] == 0 and past_value_black_x == x:
                        if y < past_value_black_y and y < 7 and board[x][y + 1] == 1 or y < 7 and board[x][y + 1] == 3:
                            black_cell, not_empty_cell = 0, 0
                            old_y = past_value_black_y
                            for index in range(past_value_black_y, y, -1):
                                black_cell += 1
                                if board[x][past_value_black_y] != 0:
                                    not_empty_cell += 1
                                past_value_black_y -= 1
                            if not_empty_cell == 2:
                                board[x][y] = 4
                                board[past_value_black_x][old_y] = 0
                                board[x][y + 1] = 0
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                if capBlackDamCollectSides["Up"]:
                    if board[past_value_black_x][past_value_black_y] == 4 and past_value_black_x > 1 and \
                            board[x][y] == 0 and past_value_black_y == y:
                        if (x < past_value_black_x and x < 7 and board[x + 1][y] == 1) or (
                                x < 7 and board[x + 1][y] == 3):
                            black_cell, not_empty_cell = 0, 0
                            old_x = past_value_black_x
                            for index in range(past_value_black_x, x, -1):
                                black_cell += 1
                                if board[past_value_black_x][y] != 0:
                                    not_empty_cell += 1
                                past_value_black_x -= 1
                            if not_empty_cell == 2:
                                board[x][y] = 4
                                board[old_x][past_value_black_y] = 0
                                board[x + 1][y] = 0
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                if capBlackDamCollectSides["Right"]:
                    if board[past_value_black_x][past_value_black_y] == 4 and past_value_black_y < 6 and \
                            board[x][y] == 0 and past_value_black_x == x:
                        if (y > past_value_black_y and board[x][y - 1] == 1) or board[x][y - 1] == 3:
                            black_cell, not_empty_cell = 0, 0
                            old_y = past_value_black_y
                            for index in range(y, past_value_black_y, -1):
                                black_cell += 1
                                if board[x][past_value_black_y] != 0:
                                    not_empty_cell += 1
                                past_value_black_y += 1
                            if not_empty_cell == 2:
                                board[x][y] = 4
                                board[past_value_black_x][old_y] = 0
                                board[x][y - 1] = 0
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                if capBlackDamCollectSides["Down"]:
                    if past_value_black_x < 7 and board[past_value_black_x][past_value_black_y] == 4 and \
                            board[x][y] == 0 and past_value_black_y == y:
                        if board[x - 1][y] == 3 or (x > past_value_black_x and board[x - 1][y] == 1):
                            black_cell, not_empty_cell = 0, 0
                            old_x = past_value_black_x
                            for index in range(x, past_value_black_x, -1):
                                black_cell += 1
                                if board[past_value_black_x][y] != 0:
                                    not_empty_cell += 1
                                past_value_black_x += 1
                            if not_empty_cell == 2:
                                board[x][y] = 4
                                board[old_x][past_value_black_y] = 0
                                board[x - 1][y] = 0
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                capBlackDamCollect = False
                checking_checkers(2)
                checking_checkers_king(2)
                if capBlackDamCollect == False:
                    move_of_white = True
            if capBlackCollect:
                if capBlackCollectSides["Left"]:
                    if board[past_value_black_x][past_value_black_y] == 2 and past_value_black_y > 1 and (
                            board[past_value_black_x][past_value_black_y - 1] == 1 or
                            board[past_value_black_x][past_value_black_y - 1] == 3) and board[x][y] == 0 and \
                            board[past_value_black_x][
                                past_value_black_y - 2] == 0 and past_value_black_x == x and past_value_black_y == y + 2:
                        board[past_value_black_x][y + 2] = 0
                        board[x][y + 1] = 0
                        board[x][y] = 2
                        checkingProgress = True
                        number_of_whites -= 1
                        draw_board(-1, -1)
                if capBlackCollectSides["Up"]:
                    if board[past_value_black_x][past_value_black_y] == 2 and past_value_black_x > 1 and (
                            board[past_value_black_x - 1][y] == 1 or board[past_value_black_x - 1][y] == 3) and \
                            board[x][y] == 0  and past_value_black_x == x + 2 and past_value_black_y == y:
                        board[x + 2][y] = 0
                        board[x + 1][y] = 0
                        board[x][y] = 2
                        checkingProgress = True
                        number_of_whites -= 1
                        draw_board(-1, -1)
                if capBlackCollectSides["Right"]:
                    if board[past_value_black_x][past_value_black_y] == 2 and past_value_black_y < 6 and (
                            board[past_value_black_x][past_value_black_y + 1] == 1 or
                            board[past_value_black_x][past_value_black_y + 1] == 3) and board[x][y] == 0 and \
                            board[past_value_black_x][
                                past_value_black_y + 2] == 0 and past_value_black_x == x and past_value_black_y == y - 2:
                        board[past_value_black_x][y - 2] = 0
                        board[x][y - 1] = 0
                        board[x][y] = 2
                        checkingProgress = True
                        number_of_whites -= 1
                        draw_board(-1, -1)
                if capBlackCollectSides["Down"]:
                    if board[past_value_black_x][past_value_black_y] == 2 and past_value_black_x < 6 and (
                            board[past_value_black_x + 1][y] == 1 or board[past_value_black_x + 1][y] == 3) and \
                            board[x][y] == 0 and board[x - 2][y] == 2 and past_value_black_y == y and past_value_black_x == x - 2:
                        if past_value_black_x == 5 and x == 7:
                            board[x][y] = 4
                        else:
                            board[x][y] = 2
                        board[x - 2][y] = 0
                        board[x - 1][y] = 0
                        checkingProgress = True
                        number_of_whites -= 1
                        draw_board(-1, -1)
                capBlackCollect = False
                checking_checkers(2)
                checking_checkers_king(2)
                if capBlackCollect == False and capBlackDamCollect == False:
                    move_of_white = True

            if skippingFriend:
                if skippingFriendSides["Left"]:
                    if board[past_value_black_x][past_value_black_y] == 2 and past_value_black_y > 1 and (
                            board[past_value_black_x][past_value_black_y - 1] == 2 or
                            board[past_value_black_x][past_value_black_y - 1] == 4) and board[x][y] == 0 and \
                            board[past_value_black_x][
                                past_value_black_y - 2] == 0 and past_value_black_x == x and past_value_black_y == y + 2:
                        board[past_value_black_x][y + 2] = 0
                        board[x][y] = 2
                        draw_board(-1, -1)
                        move_of_white = True
                if skippingFriendSides["Right"]:
                    if board[past_value_black_x][past_value_black_y] == 2 and past_value_black_y < 6 and (
                            board[past_value_black_x][past_value_black_y + 1] == 2 or
                            board[past_value_black_x][past_value_black_y + 1] == 4) and board[x][y] == 0 and \
                            board[past_value_black_x][
                                past_value_black_y + 2] == 0 and past_value_black_x == x and past_value_black_y == y - 2:
                        board[past_value_black_x][y - 2] = 0
                        board[x][y] = 2
                        draw_board(-1, -1)
                        move_of_white = True
                if skippingFriendSides["Down"]:
                    if board[past_value_black_x][past_value_black_y] == 2 and past_value_black_x < 6 and (
                            board[past_value_black_x + 1][y] == 2 or board[past_value_black_x + 1][y] == 4) and \
                            board[x][y] == 0 and board[x - 2][y] == 2 and past_value_black_x == x - 2 and past_value_black_y == y:
                        if past_value_black_x == 5 and x == 7:
                            board[x][y] = 4
                        else:
                            board[x][y] = 2
                        board[x - 2][y] = 0
                        draw_board(-1, -1)
                        move_of_white = True
                checking_checkers(2)
                checking_checkers_king(2)
            checking_checkers(2)
            checking_checkers_king(2)
            possibility_walk(x, y, 2)
            checking_the_end()
            if abilGoWalkBlack:
                if (board[past_value_black_x][past_value_black_y] != 0
                    and past_value_black_y + 1 == y and past_value_black_x == x) or \
                        (past_value_black_y - 1 == y and past_value_black_x == x) or \
                        (past_value_black_x + 1 == x and past_value_black_y == y):
                    if board[x][y] == 0 and capBlackCollect == False and capBlackDamCollect == False:
                        if board[past_value_black_x][past_value_black_y] == 2:
                            if x == 7:
                                board[x][y] = 4
                            else:
                                board[x][y] = 2
                            board[past_value_black_x][past_value_black_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = True
                if board[past_value_black_x][past_value_black_y] == 4 and board[x][
                    y] == 0 and capBlackCollect == False and capBlackDamCollect == False:
                    if past_value_black_x > x and past_value_black_y == y:
                        black_cell, not_empty_cell = 0, 0
                        old_x = past_value_black_x
                        for index in range(past_value_black_x, x, -1):
                            black_cell += 1
                            if board[past_value_black_x][y] != 0:
                                not_empty_cell += 1
                            past_value_black_x -= 1
                        if not_empty_cell == 1:
                            board[x][y] = 4
                            board[old_x][past_value_black_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = True
                    if past_value_black_x < x and past_value_black_y == y:
                        black_cell, not_empty_cell = 0, 0
                        old_x = past_value_black_x
                        for index in range(past_value_black_x, x):
                            black_cell += 1
                            if board[past_value_black_x][y] != 0:
                                not_empty_cell += 1
                            past_value_black_x += 1
                        if not_empty_cell == 1:
                            board[x][y] = 4
                            board[old_x][past_value_black_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = True
                    if past_value_black_y > y and past_value_black_x == x:
                        black_cell, not_empty_cell = 0, 0
                        old_y = past_value_black_y
                        for index in range(past_value_black_y, y, -1):
                            black_cell += 1
                            if board[x][past_value_black_y] != 0:
                                not_empty_cell += 1
                            past_value_black_y -= 1
                        if not_empty_cell == 1:
                            board[x][y] = 4
                            board[past_value_black_x][old_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = True
                    if past_value_black_y < y and past_value_black_x == x:
                        black_cell, not_empty_cell = 0, 0
                        old_y = past_value_black_y
                        for index in range(past_value_black_y, y):
                            black_cell += 1
                            if board[x][past_value_black_y] != 0:
                                not_empty_cell += 1
                            past_value_black_y += 1
                        if not_empty_cell == 1:
                            board[x][y] = 4
                            board[past_value_black_x][old_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = True
        checking_the_end()
select_move()
new_game()
draw_board(-1, -1)
canvas.bind("<Button-1>", stroke_processing)
ws.mainloop()
