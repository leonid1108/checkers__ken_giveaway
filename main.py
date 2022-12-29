from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time, random, binascii
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

Game = False

AI = True
start_game_time = time.time()
result_time = 0
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

# Воз-ть белых забрать
capWhiteCollect = False
capWhiteCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}
# Воз-ть белых дамок забрать
capWhiteDamCollect = False
capWhiteDamCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}
# Воз-ть чёрных забрать
capBlackCollect = False
capBlackCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}
# Воз-ть чёрных дамок забрать
capBlackDamCollect = False
capBlackDamCollectSides = {
    "Left": False,
    "Up": False,
    "Right": False,
    "Down": False
}

black_che = PhotoImage(file='src\\ch\\black_checkers.png')
white_che = PhotoImage(file='src\\ch\\white_checkers.png')
white_dam = PhotoImage(file='src\\ch\\white_checkers_king.png')
black_dam = PhotoImage(file='src\\ch\\black_checkers_king.png')

checkers = [0, white_che, black_che, white_dam, black_dam]

def select_move():
    global move_of_white
    if askyesno("Выбор хода", "Ход за белыми?"):
        move_of_white = True
    else:
        move_of_white = False


def new_game():
    global board
    start_game_time = time.time()
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
             [2, 2, 2, 2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2, 2, 2, 2],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
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
    global move_of_white, end_game_time, start_game_time, result_time
    # draw_board(-1, -1)

    if number_of_whites == 0:
        end_game_time = time.time()
        messagebox.showinfo(title="White's Victory", message="Победили белые!", icon='info')
        move_of_white = True
        win_white += 1
        result_time = round(end_game_time - start_game_time, 2)
        start_new()

    if number_of_blacks == 0:
        end_game_time = time.time()
        messagebox.showinfo(title="Black's victory", message="Победили чёрные!", icon="info")
        move_of_white = False
        win_black += 1
        start_new()

    if numberMovesDraw == 10 and checkingProgress is False:
        end_game_time = time.time()
        messagebox.showinfo(title="Draw!", message="Ничья!\nЗа 10 ходов не было ни одной жертвы!", icon="info")
        move_of_white = None
        start_new()


def draw_board(position_x_1, position_y_1):
    global checkers, board, move_of_white
    x = 0

    canvas.delete('all')
    canvas.create_rectangle(1200, 0, 800, 1000, fill="#505050")

    canvas.create_text(980, 125, fill="white", font="Open 18 bold", text=f"Количество белых шашек:\n{number_of_whites}")
    canvas.create_text(985, 225, fill="white", font="Open 18 bold",
                       text=f"Количество чёрных шашек:\n{number_of_blacks}")

    canvas.create_text(1000, 400, fill="white", font="Open 16 bold", text="Белые || Чёрные")
    canvas.create_text(995, 425, fill="white", font="Open 16 bold", text=f"{win_white}:{win_black}")
    if move_of_white:
        canvas.create_text(995, 500, fill="white", font="Open 16 bold", text="Ход белых")
    if move_of_white is False:
        canvas.create_text(995, 500, fill="white", font="Open 16 bold", text="Ход черных")
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


def possibility_walk_white(x, y):
    global abilGoWalkWhite
    global past_value_white_x, past_value_white_y
    global past_value_black_x, past_value_black_y
    global move_of_white

    if board[x][y] == 1:  # Для белой шашки
        if (board[x][y - 1] == 0 and y > 0) or (board[x - 1][y] == 0 and x > 0) or (y < 7 and board[x][y + 1] == 0):
            abilGoWalkWhite = True
        else:
            abilGoWalkWhite = False
        past_value_white_x = x
        past_value_white_y = y
    if board[x][y] == 3:  # Для белой дамки
        if (x < 7 and board[x + 1][y] == 0) or (x > 0 and board[x - 1][y] == 0) or (
                board[x][y - 1] == 0 and y > 0) or (
                y < 7 and board[x][y + 1] == 0):
            abilGoWalkWhite = True
        else:
            abilGoWalkWhite = False
        past_value_white_x = x
        past_value_white_y = y


def possibility_walk_black(x, y):
    global abilGoWalkBlack
    global past_value_white_x, past_value_white_y
    global past_value_black_x, past_value_black_y

    if board[x][y] == 2:  # Для чёрной шашки
        if (board[x + 1][y] == 0 and x < 7) or \
                (board[x][y + 1] == 0 and y < 8) \
                or (board[x][y - 1] == 0 and y > 0):
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

# Для белых
def checking_checkers_white():
    global skippingFriend, skippingFriendSides
    global capWhiteCollect, capWhiteCollectSides


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
                    and board[x][y - 2] == 0:  # Для перепрыгивания белой шашки влево
                skippingFriend = True
                skippingFriendSides["Left"] = True
            if (board[x][y] == 1 and x > 1) and (board[x - 1][y] == 1 or board[x - 1][y] == 3) \
                    and board[x - 2][y] == 0:  # Для перепрыгивания белой шашки вверх
                skippingFriend = True
                skippingFriendSides["Up"] = True
            if (board[x][y] == 1 and y < 6) and (board[x][y + 1] == 1 or board[x][y + 1] == 3) \
                    and board[x][y + 2] == 0:  # Для перепрыгивания белой шашки вправо
                skippingFriend = True
                skippingFriendSides["Right"] = True


# Для чёрных
def checking_checkers_black():
    global skippingFriend, skippingFriendSides
    global capBlackCollect, capBlackCollectSides

    for x in range(8):
        for y in range(8):
            if (board[x][y] == 2 and y > 1) and (board[x][y - 1] == 1 or board[x][y - 1] == 3) \
                    and board[x][y - 2] == 0:  # Для чёрной шашки влево
                capBlackCollectSides["Left"] = True
                capBlackCollect = True
            if (board[x][y] == 2 and x > 1) and (board[x - 1][y] == 1 or board[x - 1][y] == 3) \
                    and board[x - 2][y] == 0:  # Для чёрной шашки вверх
                capBlackCollect = True
                capBlackCollectSides["Up"] = True
            if (board[x][y] == 2 and y < 6) and (board[x][y + 1] == 1 or board[x][y + 1] == 3) \
                    and board[x][y + 2] == 0:  # Для чёрной шашки вправо
                capBlackCollect = True
                capBlackCollectSides["Right"] = True
            if (board[x][y] == 2 and x < 6) and (board[x + 1][y] == 1 or board[x + 1][y] == 3) \
                    and board[x + 2][y] == 0:  # Для чёрной шашки вниз
                capBlackCollectSides["Down"] = True
                capBlackCollect = True

            if (board[x][y] == 2 and y > 1) and (board[x][y - 1] == 2 or board[x][y - 1] == 4) \
                    and board[x][y - 2] == 0:  # Для перепрыгивания чёрной шашки влево
                skippingFriend = True
                skippingFriendSides["Left"] = True
            if (board[x][y] == 2 and y < 6) and (board[x][y + 1] == 2 or board[x][y + 1] == 4) \
                    and board[x][y + 2] == 0:  # Для перепрыгивания чёрной шашки вправо
                skippingFriend = True
                skippingFriendSides["Right"] = True
            if (board[x][y] == 2 and x < 6) and (board[x + 1][y] == 2 or board[x + 1][y] == 4) \
                    and board[x + 2][y] == 0:  # Для перепрыгивания чёрной шашки вниз
                skippingFriend = True
                skippingFriendSides["Down"] = True


def checking_checkers_king_white():
    global capWhiteDamCollect, capWhiteDamCollectSides
    for x in range(8):
        for y in range(8):
            if board[x][y] == 3 and y > 1:
                for index in range(8):
                    empty_cell, black_cell, count = 0, 0, 0
                    if board[x][index] == 0 and (
                            index < 6 and board[x][index + 2] == 0 or index < 6 and board[x][index + 2] == 3) and (
                            (index < 7 and board[x][index + 1] == 2) or (index < 7 and board[x][index + 1] == 4)):
                        while board[x][index] != 3:


                            if index < 7 and board[x+1][y] == 3:
                                capWhiteDamCollectSides["Left"] = True
                                capWhiteDamCollect = True
                                break
                                print("sssssssssssssss")
                                black_cell += 1
                                if index < 7:
                                    index += 1
                                else:
                                    break
                                if board[x][index] == 0:
                                    empty_cell += 1
                                if board[x][index] == 2 or board[x][index] == 4 and index > 0:
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
                            if empty_cell == black_cell - 2 and board[x][index] == 3 and index < 7:
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

def checking_checkers_king_black():
    global capBlackDamCollect, capBlackDamCollectSides
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


def computer():
    global move_of_white, numberMovesDraw, checkingProgress
    global number_of_whites, number_of_blacks, AI, Game

    global capBlackCollect, capBlackCollectSides
    global capBlackDamCollect, capBlackDamCollectSides

    global past_value_black_x_AI, past_value_black_y_AI, x_ai, y_ai
    global abilGoWalkBlack, skippingFriend, skippingFriendSides
    Game = True

    if checkingProgress == True:
        checkingProgress = False
        numberMovesDraw = 0
    if AI:
        checking_the_end()
        fear = True
        capBlackCollect = False
        capBlackDamCollect = False
        checking_checkers_black()
        checking_checkers_king_black()
        abilGoWalkBlack = False
        past_value_black_x_AI = 0
        past_value_black_y_AI = 0
        x_ai, y_ai = 0, 0

        if capBlackCollect or capBlackDamCollect:
            fear = False
        else:
            fear = True

        while abilGoWalkBlack != True:
            try:
                count = 0
                random_checker = random.randint(1, str(board).count('2'))
            except IndexError:
                random_checker = random.randint(1, str(board).count('2'))
            for x in range(8):
                for y in range(8):
                    if board[x][y] == 2 and count != random_checker:
                        count += 1
                        if count == random_checker:
                            past_value_black_x_AI = x
                            past_value_black_y_AI = y
                            try:
                                possibility_walk_black(past_value_black_x_AI, past_value_black_y_AI)
                            except IndexError:
                                continue

            checking_checkers_black()
            checking_checkers_king_black()
            if abilGoWalkBlack and capBlackCollect is False and capBlackDamCollect is False and fear:
                checking_checkers_black()
                checking_checkers_king_black()
                if past_value_black_y_AI > 0 and board[past_value_black_x_AI][past_value_black_y_AI - 1] == 0 and \
                        board[past_value_black_x_AI][
                            past_value_black_y_AI] == 2 and capBlackCollect is False and capBlackDamCollect is False:
                    board[past_value_black_x_AI][past_value_black_y_AI] = 0
                    board[past_value_black_x_AI][past_value_black_y_AI - 1] = 2
                    x_ai = past_value_black_x_AI
                    y_ai = past_value_black_y_AI - 1
                    numberMovesDraw += 1
                elif past_value_black_y_AI < 7 and board[past_value_black_x_AI][past_value_black_y_AI + 1] == 0 and \
                        board[past_value_black_x_AI][
                            past_value_black_y_AI] == 2 and capBlackCollect is False and capBlackDamCollect is False:
                    board[past_value_black_x_AI][past_value_black_y_AI] = 0
                    board[past_value_black_x_AI][past_value_black_y_AI + 1] = 2
                    x_ai = past_value_black_x_AI
                    y_ai = past_value_black_y_AI + 1
                    numberMovesDraw += 1
                elif past_value_black_x_AI < 7 and board[past_value_black_x_AI + 1][past_value_black_y_AI] == 0 and \
                        board[past_value_black_x_AI][
                            past_value_black_y_AI] == 2 and capBlackCollect is False and capBlackDamCollect is False:
                    board[past_value_black_x_AI][past_value_black_y_AI] = 0
                    if past_value_black_x_AI == 6:
                        board[past_value_black_x_AI + 1][past_value_black_y_AI] = 4
                    else:
                        board[past_value_black_x_AI + 1][past_value_black_y_AI] = 2
                    x_ai = past_value_black_x_AI + 1
                    y_ai = past_value_black_y_AI
                    numberMovesDraw += 1
                move_of_white = True
                draw_board(-1, -1)
                abilGoWalkBlack = False
                break
            checking_checkers_black()
            checking_checkers_king_black()
            if capBlackDamCollect:
                checking_checkers_black()
                checking_checkers_king_black()

                if capBlackDamCollectSides["Up"]:
                    for x in range(8):
                        for y in range(8):
                            if x > 1 and board[x][y] == 4:
                                for index in range(8):
                                    zero_count, bl_count, count = 0, 0, 0
                                    if board[index][y] == 0 and ((index < 7 and board[index + 1][y] == 1) or (
                                            index < 7 and board[index + 1][y] == 3)) and (
                                            index < 6 and board[index + 2][y] == 0 or index < 6 and board[index + 2][
                                        y] == 4):
                                        while board[index][y] != 4:
                                            if x < 7 and board[x + 1][y] == 4:
                                                board[x + 1][y] = 0
                                                board[x][y] = 0
                                                board[x - 1][y] = 4
                                                checkingProgress = True
                                                number_of_whites -= 1
                                                draw_board(-1, -1)
                                                move_of_white = True
                                                checking_checkers_black()
                                                checking_checkers_king_black()
                                                break
                                            bl_count += 1
                                            if index < 7:
                                                index += 1
                                            else:
                                                break
                                            if board[index][y] == 0:
                                                zero_count += 1
                                            if board[index][y] == 1 or board[index][y] == 3:
                                                count += 1
                                                indextwo = index
                                                j2 = y
                                            if count == 2:
                                                break
                                            if zero_count == bl_count - 2 and board[index][y] == 4:
                                                board[index][y] = 0
                                                board[indextwo][j2] = 0
                                                board[indextwo - 1][j2] = 4
                                                checkingProgress = True
                                                number_of_whites -= 1
                                                draw_board(-1, -1)
                                                move_of_white = True
                                                checking_checkers_black()
                                                checking_checkers_king_black()
                                                break
                checking_checkers_black()
                checking_checkers_king_black()
                if capBlackDamCollectSides["Down"]:
                    for x in range(8):
                        for y in range(8):
                            if x < 7 and board[x][y] == 4:
                                for index in range(8):
                                    zero_count, bl_count = 0, 0
                                    if board[index][y] == 0 and (
                                            (index > 1 and board[index - 1][y] == 1) or (
                                            index > 1 and board[index - 1][y] == 3)):
                                        while board[index][y] != 4:
                                            bl_count += 1
                                            index -= 1
                                            if board[index][y] == 0:
                                                zero_count += 1
                                            if board[index][y] == 1 or board[index][y] == 3:
                                                indextwo = index
                                                j2 = y
                                            if board[index][y] == 4 and zero_count == bl_count - 2:
                                                board[index][y] = 0
                                                board[indextwo][j2] = 0
                                                board[indextwo + 1][j2] = 4
                                                checkingProgress = True
                                                number_of_whites -= 1
                                                draw_board(-1, -1)
                                                move_of_white = True
                                                checking_checkers_black()
                                                checking_checkers_king_black()
                                                break
                checking_checkers_black()
                checking_checkers_king_black()
                if capBlackDamCollectSides["Left"]:
                    for x in range(8):
                        for y in range(8):
                            if y > 1 and board[x][y] == 4:
                                for index in range(8):
                                    zero_count, bl_count, count = 0, 0, 0
                                    if board[x][index] == 0 and (
                                            (index < 7 and board[x][index + 1] == 1) or (
                                            index < 7 and board[x][index + 1] == 3)) and (
                                            index < 6 and board[x][index + 2] == 0 or index < 6 and board[x][
                                        index + 2] == 4):
                                        while board[x][index] != 4:
                                            if y < 7 and board[x][y + 1] == 4:
                                                board[x][y + 1] = 0
                                                board[x][y] = 0
                                                board[x][y - 1] = 4
                                                checkingProgress = True
                                                number_of_whites -= 1
                                                draw_board(-1, -1)
                                                move_of_white = True
                                                checking_checkers_black()
                                                checking_checkers_king_black()
                                                break
                                            bl_count += 1
                                            if index < 7:
                                                index += 1
                                            else:
                                                break
                                            if board[x][index] == 0:
                                                zero_count += 1
                                            if board[x][index] == 1 or board[x][index] == 3:
                                                indextwo = index
                                                ii = x
                                                count += 1
                                            if count == 2:
                                                break
                                            if zero_count == bl_count - 2 and board[x][index] == 4:
                                                board[x][index] = 0
                                                board[ii][indextwo] = 0
                                                board[ii][indextwo - 1] = 4
                                                checkingProgress = True
                                                number_of_whites -= 1
                                                draw_board(-1, -1)
                                                move_of_white = True
                                                checking_checkers_black()
                                                checking_checkers_king_black()
                                                break
                checking_checkers_black()
                checking_checkers_king_black()

                if capBlackDamCollectSides["Right"]:
                    for x in range(8):
                        for y in range(8):
                            if y < 7 and board[x][y] == 4:
                                for index in range(8):
                                    zero_count, bl_count = 0, 0
                                    if board[x][index] == 0 and (
                                            (index > 1 and board[x][index - 1] == 1) or (
                                            index > 1 and board[x][index - 1] == 3)):
                                        while board[x][index] != 4:
                                            bl_count += 1
                                            index -= 1
                                            if board[x][index] == 0:
                                                zero_count += 1
                                            if board[x][index] == 1 or board[x][index] == 3:
                                                indextwo = index
                                                ii = x
                                            if zero_count == bl_count - 2 and board[x][index] == 4:
                                                board[x][index] = 0
                                                board[ii][indextwo] = 0
                                                board[ii][indextwo + 1] = 4
                                                checkingProgress = True
                                                number_of_whites -= 1
                                                draw_board(-1, -1)
                                                move_of_white = True
                                                checking_checkers_black()
                                                checking_checkers_king_black()
                                                break
                if capBlackDamCollect is False and capBlackCollect is False:
                    move_of_white = True
                    draw_board(-1, -1)
                    break
                capBlackDamCollect = False
                checking_checkers_black()
                checking_checkers_king_black()
            checking_the_end()
            checking_checkers_black()
            checking_checkers_king_black()
            if capBlackCollect and capBlackDamCollect is False:
                if capBlackCollectSides["Up"]:
                    for x in range(8):
                        for y in range(8):
                            if (board[x][y] == 2 and x < 7) and (
                                    board[x - 1][y] == 1 or board[x - 1][y] == 3) and board[x - 2][y] == 0:
                                board[x][y] = 0
                                board[x - 1][y] = 0
                                board[x - 2][y] = 2
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                                checking_checkers_black()
                                checking_checkers_king_black()
                                move_of_white = True

                if capBlackCollectSides["Down"]:
                    for x in range(8):
                        for y in range(8):
                            if (board[x][y] == 2 and x < 6) and (
                                    board[x + 1][y] == 1 or board[x + 1][y] == 3) and board[x + 2][y] == 0:
                                board[x][y] = 0
                                board[x + 1][y] = 0
                                if x == 5:
                                    board[x + 2][y] = 4
                                else:
                                    board[x + 2][y] = 2
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                                checking_checkers_black()
                                checking_checkers_king_black()
                                move_of_white = True
                if capBlackCollectSides["Left"]:
                    for x in range(8):
                        for y in range(8):
                            if (board[x][y] == 2 and y > 1) and (
                                    board[x][y - 1] == 1 or board[x][y - 1] == 3) and board[x][y - 2] == 0:
                                board[x][y] = 0
                                board[x][y - 1] = 0
                                board[x][y - 2] = 2
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                                checking_checkers_black()
                                checking_checkers_king_black()
                                move_of_white = True
                if capBlackCollectSides["Right"]:
                    for x in range(8):
                        for y in range(8):
                            if (board[x][y] == 2 and y < 6) and (board[x][y + 1] == 1 or board[x][y + 1] == 3) and \
                                    board[x][
                                        y + 2] == 0:
                                board[x][y] = 0
                                board[x][y + 1] = 0
                                board[x][y + 2] = 2
                                checkingProgress = True
                                number_of_whites -= 1
                                draw_board(-1, -1)
                                checking_checkers_black()
                                checking_checkers_king_black()
                                move_of_white = True
                checking_the_end()
                checking_checkers_black()
                checking_checkers_king_black()
                if capBlackCollect is False and capBlackDamCollect is False:
                    move_of_white = True
                    draw_board(-1, -1)
                    break


def stroke_processing(event):
    global move_of_white, numberMovesDraw, checkingProgress
    global number_of_whites, number_of_blacks, Game

    global capWhiteCollect, capWhiteCollectSides
    global capWhiteDamCollect, capWhiteDamCollectSides
    global past_value_white_x, past_value_white_y
    draw_board(-1, -1)
    Game = True
    if checkingProgress == True:
        checkingProgress = False
        numberMovesDraw = 0
    if event.x < 800 and event.x > 0 and event.y < 800 and event.y > 0:
        x, y = event.y // 100, event.x // 100
        if move_of_white:
            if capWhiteDamCollect:
                if board[x][y] == 1 or board[x][y] == 3:
                    draw_board(-1, -1)
                    canvas.create_rectangle(y * 100, x * 100, y * 100 + 100, x * 100 + 100, outline="orange", width=3)
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
                checking_checkers_white()
                checking_checkers_king_white()
                if capWhiteDamCollect is False:
                    move_of_white = False
                    if number_of_blacks != 0:
                        computer()
            if capWhiteCollect:
                if board[x][y] == 1:
                    draw_board(-1, -1)
                    canvas.create_rectangle(y * 100, x * 100, y * 100 + 100, x * 100 + 100, outline="orange", width=3)
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
                            board[x][y] == 0 and board[x + 2][
                        y] == 1 and past_value_white_x == x + 2 and past_value_white_y == y:
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
                checking_checkers_white()
                checking_checkers_king_white()
                if capWhiteDamCollect is False and capWhiteCollect is False:
                    move_of_white = False
                    if number_of_blacks != 0:
                        computer()
            if skippingFriend:
                if board[x][y] == 1:
                    draw_board(-1, -1)
                    canvas.create_rectangle(y * 100, x * 100, y * 100 + 100, x * 100 + 100, outline="orange", width=3)
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
                        if number_of_blacks != 0:
                            computer()

                if skippingFriendSides["Up"]:
                    if board[past_value_white_x][past_value_white_y] == 1 and past_value_white_x > 1 and \
                            (board[past_value_white_x - 1][y] == 1 or board[past_value_white_x - 1][y] == 3) \
                            and board[x][y] == 0 and x < 6 and board[x + 2][
                        y] == 1 and past_value_white_x == x + 2 and past_value_white_y == y:
                        if past_value_white_x == 2 and x == 0:
                            board[x][y] = 3
                        else:
                            board[x][y] = 1
                        board[x + 2][y] = 0
                        draw_board(-1, -1)
                        move_of_white = False
                        if number_of_blacks != 0:
                            computer()
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
                        if number_of_blacks != 0:
                            computer()
                checking_checkers_white()
                checking_checkers_king_white()
            checking_checkers_white()
            checking_checkers_king_white()
            possibility_walk_white(x, y)
            checking_the_end()
            if abilGoWalkWhite:
                if (board[past_value_white_x][past_value_white_y] != 0 and past_value_white_y + 1 == y and past_value_white_x == x) or\
                        (past_value_white_y - 1 == y and past_value_white_x == x) or\
                        (past_value_white_x - 1 == x and past_value_white_y == y):
                    if board[x][y] == 0 and capWhiteCollect is False and capWhiteDamCollect is False:
                        if board[past_value_white_x][past_value_white_y] == 1:
                            if x == 0:
                                board[x][y] = 3
                            else:
                                board[x][y] = 1
                            board[past_value_white_x][past_value_white_y] = 0
                            numberMovesDraw += 1
                            draw_board(-1, -1)
                            move_of_white = False
                            if number_of_blacks != 0:
                                computer()
                if board[past_value_white_x][past_value_white_y] == 3 and board[x][
                    y] == 0 and capWhiteCollect is False and capWhiteDamCollect is False:
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
                            if number_of_blacks != 0:
                                computer()
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
                            if number_of_blacks != 0:
                                computer()
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
                            if number_of_blacks != 0:
                                computer()
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
                            if number_of_blacks != 0:
                                computer()
        else:
            computer()
        checking_the_end()


class Ui_Dialog_register(object):
    def authorization(self):
       login, password, index = 0, 0, 0
       empty_str = True
       if self.lineEdit.text() == "" or self.lineEdit_2.text() == "":
           error_lk = QMessageBox()
           error_lk.setWindowTitle("Error")
           error_lk.setText("Пустая строка!\nВведите что-нибудь.")
           error_lk.setWindowIcon(QIcon("src\\warning.png"))
           error_lk.setIcon(QMessageBox.Warning)
           error_lk.exec_()
           empty_str = False
       with open("src\\password.txt", "r+") as file:
           flag = True
           lines = file.readlines()
           for line in lines:
               if self.lineEdit.text() == (binascii.unhexlify(line.replace("\n", ""))).decode('UTF-8'):
                   login = index
                   if self.lineEdit_2.text() != (binascii.unhexlify(lines[login+1].replace("\n", ""))).decode('UTF-8'):
                       index += 2
                       continue
                   else:
                       flag = False
                       Ok = QMessageBox()
                       Ok.setWindowTitle("Вы успешно вошли в личный кабинет")
                       Ok.setText("Вход прошел успешно!")
                       Ok.setWindowIcon(QIcon("src\\ok.png"))
                       Ok.setIcon(QMessageBox.Information)
                       Ok.exec_()
                       self.lineEdit.setText("")
                       self.lineEdit_2.setText("")
                       Dialog_lk.show()
                       Dialog_register.hide()
                       break
               index += 1
           if flag and empty_str:
               error_lk = QMessageBox()
               error_lk.setWindowTitle("Error")
               error_lk.setText("Пользователь не найден.\nСоздайте аккаунт.")
               error_lk.setWindowIcon(QIcon("src\\warning.png"))
               error_lk.setIcon(QMessageBox.Warning)
               error_lk.exec_()

    def registration(self):
        def xtea_encipher(num_rounds, v, k):
            v0 = int(v[0])
            v1 = int(v[1])
            summ, delta = 0, 0x9e3779b9
            for i in range(num_rounds):
                v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (summ + k[summ & 3])
                summ = (summ + delta)
                v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (summ + k[(summ >> 11) & 3])
            v[0] = v0
            v[1] = v1
            return v
        def xtea_decipher(num_rounds, v, k):
            v0 = int(v[0])
            v1 = int(v[1])
            delta = 0x9e3779b9
            summ = (delta * (-num_rounds))
            for i in range(num_rounds):
                v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (summ + k[(summ >> 11) & 3])
                summ = (summ - delta)
                v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (summ + k[summ & 3])
            v[0] = v0
            v[1] = v1
            return v

        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "":
            error_lk = QMessageBox()
            error_lk.setWindowTitle("Error")
            error_lk.setText("Пустая строка!\nВведите что-нибудь.")
            error_lk.setWindowIcon(QIcon("src\\warning.png"))
            error_lk.setIcon(QMessageBox.Warning)
            error_lk.exec_()

        else:
            login = self.lineEdit.text().encode()
            password = self.lineEdit_2.text().encode()

            login_encryption = (binascii.hexlify(login)).decode('UTF-8')
            password_encryption = (binascii.hexlify(password)).decode('UTF-8')

            element_login = int(("0x" + login_encryption), 0)
            element_password = int(("0x" + password_encryption), 0)

            coded_login = xtea_encipher(64, [element_login, element_login, element_login, element_login],
            [0x12345678, 0x00ff00ff, 0x1111aaaa, 0x1010ffcc, 0x12345678, 0x00ff00ff, 0x1111aaaa, 0x1010ffcc])

            coded_password = xtea_encipher(64, [element_password, element_password, element_password, element_password],
            [0x12345678, 0x00ff00ff, 0x1111aaaa, 0x1010ffcc, 0x12345678, 0x00ff00ff, 0x1111aaaa, 0x1010ffcc])

            result_login = "{:x}".format(coded_login[-1])
            result_password = "{:x}".format(coded_password[-1])
            with open("src\\password.txt", "r+") as file:
                lines = file.readlines()
                flag = True
                for line in lines:
                    if self.lineEdit.text() == (binascii.unhexlify(line.replace("\n", ""))).decode('UTF-8'):
                       flag = False
                if flag:
                    file.write(f"\n{result_login}\n")
                    file.write(f"{result_password}\n")
                    Ok = QMessageBox()
                    Ok.setWindowTitle("Вы зарегистрировались")
                    Ok.setText("Регистрация прошла успешно!")
                    Ok.setWindowIcon(QIcon("src\\ok.png"))
                    Ok.setIcon(QMessageBox.Information)
                    Ok.exec_()
                else:
                    error = QMessageBox()
                    error.setWindowTitle("Error")
                    error.setText("Пользователь с данным именем уже существует.")
                    error.setWindowIcon(QIcon("src\\warning.png"))
                    error.setIcon(QMessageBox.Warning)
                    error.exec_()
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.label_2.setText("Войдите в аккаунт")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1121, 880)
        Dialog.setStyleSheet("background-color: rgb(95, 95, 95);\nborder-radius: 10px;")
        Dialog.setWindowIcon(QtGui.QIcon('src\\login.png'))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(480, 40, 200, 200))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("src\\logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(280, 270, 600, 511))
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QtCore.QRect(90, 50, 421, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_2.setMouseTracking(False)
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_2.setAcceptDrops(False)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setIndent(25)
        self.label_2.setOpenExternalLinks(False)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(90, 160, 421, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI Semilight")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit.setStyleSheet("background-color: rgb(204, 204, 204);\npadding-left: 8px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 220, 421, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI Semilight")
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_2.setStyleSheet("background-color: rgb(204, 204, 204);\npadding-left: 8px;")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(90, 370, 421, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("background-color: rgb(255, 149, 0);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 300, 421, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 149, 0);")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton_2.clicked.connect(self.authorization)
        self.pushButton.clicked.connect(self.registration)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Регистрация"))
        self.label_2.setText(_translate("Dialog", "Создать аккаунт"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Имя пользователя"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Пароль"))
        self.pushButton.setText(_translate("Dialog", "Зарегистрироваться"))
        self.pushButton_2.setText(_translate("Dialog", "Войти"))

class Ui_Dialog_lk(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(750, 570)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);\nborder-radius: 10px;")
        Dialog.setWindowIcon(QtGui.QIcon('src\\login.png'))
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(612, 487, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                        "border-radius: 4;\n"
                                        "color: white;\n"
                                        "\n"
                                        "")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(260, 200, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("background-color: rgb(255, 149, 0);\n"
                                      "border-radius: 4;\n"
                                      "color: black;\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 460, 191, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("background-color: rgb(95, 95, 95);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-radius: 6;\n"
                                        "")
        self.pushButton_3.setObjectName("pushButton_3")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(210, 310, 331, 121))
        self.frame.setStyleSheet("background-color: rgb(80, 80, 80);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 140, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(170, 60, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")

        self.pushButton.clicked.connect(self.open_game)
        self.pushButton_2.clicked.connect(self.close_form)
        self.pushButton_3.clicked.connect(self.show_stat)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def show_stat(self):
        self.label_2.setHidden(False)
        self.label_3.setHidden(False)
        if Game:
            self.label_2.setText(f"Время: {result_time} секунд")
            self.label_3.setText(f"Счёт: {win_white}")
        else:
            self.label_2.setText(f"Время: 0 секунд")
            self.label_3.setText(f"Счёт: 0")

    def open_game(self):
        select_move()
        new_game()
        draw_board(-1, -1)
        canvas.bind("<Button-1>", stroke_processing)
        ws.mainloop()

    def close_form(self):
        Dialog_lk.hide()
        Dialog_register.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Регистрация"))
        self.pushButton_2.setText(_translate("Dialog", "Выход"))
        self.pushButton.setText(_translate("Dialog", "ИГРАТЬ В КЕНЫ-ПОДДАВКИ С ИИ"))
        self.pushButton_3.setText(_translate("Dialog", "Показать статистику"))
        self.label.setText(_translate("Dialog", "Лучший результат:"))
        self.label_2.setText(_translate("Dialog", ""))
        self.label_3.setText(_translate("Dialog", ""))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_register = QtWidgets.QDialog()
    Dialog_lk = QtWidgets.QDialog()
    regui = Ui_Dialog_register()
    lkui = Ui_Dialog_lk()
    regui.setupUi(Dialog_register)
    lkui.setupUi(Dialog_lk)
    Dialog_register.show()
    sys.exit(app.exec_())
