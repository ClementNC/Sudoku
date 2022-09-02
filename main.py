import pygame
import random
from board import solve, is_valid, find_all_empty
from button import Button, AddOn
from sudoku_generator import generate_board
from main_menu import pause
import os
import time
pygame.font.init()

os.chdir("C:/Users/William/Documents/Clement/Python/Sudoku")


# Load images
undo_img = pygame.image.load(os.path.join('images', 'undo.png'))
erase_img = pygame.image.load(os.path.join('images', 'erase.png'))
notes_img = pygame.image.load(os.path.join('images', 'notes.png'))
hint_img = pygame.image.load(os.path.join('images', 'hint.png'))
easy_img = pygame.image.load(os.path.join('images', 'easy.png'))
medium_img = pygame.image.load(os.path.join('images', 'medium.png'))
hard_img = pygame.image.load(os.path.join('images', 'hard.png'))
pause_img = pygame.image.load(os.path.join('images', 'pause.png'))
# quit_img = pygame.image.load(os.path.join('images', 'quit.png'))

# undo = Button(100,540, undo_img, 0.5)
erase = AddOn(200,540, erase_img, 0.5)
notes = AddOn(300,540,notes_img, 0.5)
# hint = AddOn(400, 540, hint_img, 0.5)
easy = Button(540/2 - easy_img.get_width()/2, 200, easy_img, 1)
medium = Button(540/2 - medium_img.get_width()/2, 300, medium_img, 1)
hard = Button(540/2 - hard_img.get_width()/2, 400, hard_img, 1)
pause = Button(10, 530, pause_img, 0.7)
# quit_btn = Button(540/2 - quit_img.get_width()/2, 500, quit_img, 1)

WIN = pygame.display.set_mode((520,650))
pygame.display.set_caption("Sudoku")


class Grid:
    def __init__(self, level, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.board = generate_board(level)
        self.cells = [[Cell(int(self.board[i][j]), i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        

    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def note_check(self, row, col):
        for r in range(9):
            remove_notes = []
            for num in self.cells[r][col].note:
                if not (is_valid((r,col), num, self.model)):
                    remove_notes.append(num)
            for num in remove_notes:
                self.cells[r][col].note.remove(num)
        
        for c in range(9):
            remove_notes = []
            for num in self.cells[row][c].note:
                if not (is_valid((row,c), str(num), self.model)):
                    remove_notes.append(num)
            for num in remove_notes:
                self.cells[row][c].note.remove(num)

        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                for num in self.cells[i][j].note:
                    if not (is_valid((i, j), str(num), self.model)):
                        self.cells[i][j].note.remove(num)

    def place(self, val):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set(val)
            self.cells[row][col].note = []
            self.update_model()
            # self.note_check(row, col)

            if is_valid((row,col), str(val), self.model) and solve(self.model):
                return True
            else:
                self.cells[row][col].set(0)
                self.cells[row][col].note = []
                self.update_model()
                return False

    def take_note(self, row, col, val):
        self.cells[row][col].set_note(int(val))

            
            

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].note = []

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True


class Cell:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.note = []
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        note_font = pygame.font.SysFont("comicsans", 12)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if len(self.note) > 0 and self.value == 0:
            for num in self.note:
                text = note_font.render(str(num), 1, (128,128,128))
                if num <= 3:
                    if num % 3 == 0:
                        win.blit(text, (x+45, y+3))
                    elif num % 3 == 1:
                        win.blit(text, (x+5, y+3))
                    else:
                        win.blit(text, (x+24, y+3))
                elif num <= 6:
                    if num % 3 == 0:
                        win.blit(text, (x+45, y+23))
                    elif num % 3 == 1:
                        win.blit(text, (x+5, y+23))
                    else:
                        win.blit(text, (x+24, y+23))
                else:
                    if num % 3 == 0:
                        win.blit(text, (x+45, y+42))
                    elif num % 3 == 1:
                        win.blit(text, (x+5, y+42))
                    else:
                        win.blit(text, (x+24, y+42))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_note(self, val):
        if not val in self.note:
            self.note.append(val)
        else:
            self.note.remove(val)


def redraw_window(win, board, time, strikes, hint_count):
    WIN.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 20)
    # hint_font = pygame.font.SysFont("arial", 15)
    # hint_text = hint_font.render(f"{hint_count}x", 1, (0, 100, 205))
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    WIN.blit(text, (520 - 110, 610))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    WIN.blit(text, (20, 610))
    # win.blit(hint_text, (413,580))
    # Draw grid and board
    board.draw(win)
    erase.draw(win)
    notes.draw(win)
    pause.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main(level):
    grid = Grid(level, 9,9,520,520)
    key = None
    run = True
    start = time.time()
    hint_count = 3
    strikes = 0
    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    grid.select(clicked[0], clicked[1])
                    key = None

        if notes.get_clicked():
            if notes.is_on:
                notes.is_on = False
            else:
                notes.is_on = True
        
        if erase.get_clicked():
            if erase.is_on:
                erase.is_on = False
            else:
                erase.is_on = True


        if erase.is_on:
            i,j = grid.selected
            if grid.board[i][j] == '0':
                grid.clear()

        if not notes.is_on and key != None:
            i,j = grid.selected
            if grid.place(key):
                print("Success")
            else:
                print("Wrong")
                grid.cells[i][j].set(0)
                grid.update_model()
                strikes += 1
            key = None

            if grid.is_finished() or strikes == 3:
                print("Game over")
                run = False

        elif notes.is_on and key != None:
            i,j = grid.selected
            grid.take_note(i,j,key)
            key = None

        # if pause.get_clicked():
        #     pause()

        redraw_window(WIN, grid, play_time, strikes, hint_count)
        pygame.display.update()

def main_menu():
    run = True
    title_font = pygame.font.SysFont("comicsans", 50)
    title = title_font.render("Sudoku", 1, (143, 199, 245))
    while run:
        # quit_btn.draw(win)
        if easy.get_clicked():
            print("easy")
            main("easy")
        elif medium.get_clicked():
            print("medium")
            main("medium")
        elif hard.get_clicked():
            print("hard")
            main("hard")
        # elif quit_btn.get_clicked():
        #     run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        WIN.fill((255,255,255))
        WIN.blit(title, (540/2 - title.get_width()/2, 10))
        easy.draw(WIN)
        medium.draw(WIN)
        hard.draw(WIN)
        pygame.display.update()


if __name__ == "__main__":
    main_menu()
    pygame.quit()