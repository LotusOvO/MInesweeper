import sys
import pygame
import random
import time
import InputBox
import tkinter
from tkinter import messagebox

SIZE = 30
mes = 1
root = tkinter.Tk()
root.withdraw()


def drawText(screen, font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


class Mine:
    def __init__(self, x, y, value=0):
        self.x = x
        self.y = y
        self.value = value
        self.aroundmine = -1
        # 0-未点击 1-已点击 2-地雷 3-标记 4-问号 5-爆炸
        self.status = 0


class MineBlock:
    def __init__(self, x, y):
        self.c = x
        self.r = y
        self.block = [[Mine(i, j) for j in range(y)] for i in range(x)]
        self.created = 0

    def creatmine(self, x, y, num):
        for i in random.sample(range(self.r * self.c - 1), num):
            if i % self.c == x and i // self.c == y:
                self.block[self.c - 1][self.r - 1].value = 1
            else:
                self.block[i % self.c][i // self.c].value = 1
        self.created = 1

    def doubleclick(self, x, y):
        around = self.getaround(x, y)
        count_flag = 0
        for i, j in around:
            if self.block[i][j].status == 3:
                count_flag += 1
        if count_flag == self.block[x][y].aroundmine:
            for i, j in around:
                if self.block[i][j].status == 0:
                    if not self.openmine(i, j):
                        return False
        return True

    def openmine(self, x, y):
        if self.block[x][y].value == 1:
            self.block[x][y].status = 5
            return False

        self.block[x][y].status = 1

        around = self.getaround(x, y)
        summine = 0
        for i, j in around:
            if self.block[i][j].value == 1:
                summine += 1
        self.block[x][y].aroundmine = summine

        if summine == 0:
            for i, j in around:
                if self.block[i][j].aroundmine == -1:
                    self.openmine(i, j)

        return True

    def getaround(self, x, y):
        return [(i, j) for i in range(max(0, x - 1), min(x + 2, self.c))
                for j in range(max(0, y - 1), min(y + 2, self.r))
                if i != x or j != y]


pygame.init()
row = 10
col = 20
minenum = 20
size = width, height = col * SIZE, row * SIZE + 60
screen = pygame.display.set_mode(size)
pygame.display.set_caption("扫雷")
font = pygame.font.Font("./resources/simhei.ttf", SIZE * 2)
font_sm = pygame.font.Font("./resources/simhei.ttf", 20)
fwidth, fheight = font.size("999")
red = (200, 40, 40)
clock = pygame.time.Clock()
color = (255, 255, 255)

# 0-失败 1-准备 2-游戏 3-胜利
game_status = 1

mine_num = []
for i in range(9):
    img = pygame.image.load("./resources/" + str(i) + ".png").convert()
    img = pygame.transform.smoothscale(img, (SIZE, SIZE))
    mine_num.append(img)
img_close = pygame.image.load("./resources/close.png").convert()
img_close = pygame.transform.smoothscale(img_close, (SIZE, SIZE))
img_flag = pygame.image.load("./resources/flag.png").convert()
img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
img_mine = pygame.image.load("./resources/mine.png").convert()
img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
img_question = pygame.image.load("./resources/question.png").convert()
img_question = pygame.transform.smoothscale(img_question, (SIZE, SIZE))
img_boom = pygame.image.load("./resources/boom.png").convert()
img_boom = pygame.transform.smoothscale(img_boom, (SIZE, SIZE))
img_win = pygame.image.load("./resources/win.png").convert()
img_win = pygame.transform.smoothscale(img_win, (60, 60))
img_ready = pygame.image.load("./resources/ready.png").convert()
img_ready = pygame.transform.smoothscale(img_ready, (60, 60))
img_lose = pygame.image.load("./resources/lose.png").convert()
img_lose = pygame.transform.smoothscale(img_lose, (60, 60))

mineblock = MineBlock(col, row)
begintime = 0
nowtime = 0

rowinput = InputBox.InputBox(2, pygame.Rect(10, 30, 6, 25))
colinput = InputBox.InputBox(2, pygame.Rect(65, 30, 6, 25))
numinput = InputBox.InputBox(2, pygame.Rect(120, 30, 6, 25))

submit = pygame.Rect(170, 17, 50, 30)
messagebox.showinfo("提示", "左上角调整难度\n左键打开格子\n右键切换标记\n对已打开格子右键可打开附近格子")
while True:
    clock.tick(60)
    face_pos_x = width // 2 - 30
    face_pos_y = 0
    events = pygame.event.get()
    for event in events:
        rowinput.dealEvent(event)
        colinput.dealEvent(event)
        numinput.dealEvent(event)
        x = 0
        y = 0
        ml, mm, mr = False, False, False
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            x = mx // SIZE
            y = (my - 60) // SIZE
            ml, mm, mr = pygame.mouse.get_pressed()
            if ml and not mr:
                if submit.collidepoint(event.pos):
                    if rowinput.text.isdigit() and int(rowinput.text) > 0:
                        row = int(rowinput.text)
                    else:
                        row = 10
                    if colinput.text.isdigit() and int(colinput.text) > 0:
                        col = int(colinput.text)
                    else:
                        col = 20
                    if numinput.text.isdigit() and int(numinput.text) > 0:
                        minenum = int(numinput.text)
                    else:
                        minenum = 20
                    size = width, height = col * SIZE, row * SIZE + 60
                    screen = pygame.display.set_mode(size)
                    game_status = 1
                    mineblock = MineBlock(col, row)
                if y < 0:
                    if face_pos_x <= mx <= face_pos_x + 60 and face_pos_y <= my <= face_pos_y + 60:
                        if game_status != 1:
                            mineblock = MineBlock(col, row)
                            game_status = 1
                            nowtime = 0
                            mes = 1
                else:
                    if game_status == 1:
                        mineblock.creatmine(x, y, minenum)
                        begintime = time.time()
                        game_status = 2
                    if game_status == 2:
                        if mineblock.block[x][y].status == 0:
                            if not mineblock.openmine(x, y):
                                game_status = 0
                                if mes == 1:
                                    mes = 3

            elif not ml and mr:
                if game_status == 2 and y >= 0:
                    if game_status == 2 and y >= 0:
                        if mineblock.block[x][y].status == 1:
                            if not mineblock.doubleclick(x, y):
                                game_status = 0
                    if mineblock.block[x][y].status == 0:
                        mineblock.block[x][y].status = 3
                    elif mineblock.block[x][y].status == 3:
                        mineblock.block[x][y].status = 4
                    elif mineblock.block[x][y].status == 4:
                        mineblock.block[x][y].status = 0

    screen.fill(color)
    n = 0

    count_flag = 0
    count_opened = 0
    # 渲染地雷矩阵
    for i in mineblock.block:
        for item in i:
            pos = (item.x * SIZE, item.y * SIZE + 60)
            if item.status == 1:
                screen.blit(mine_num[item.aroundmine], pos)
                count_opened += 1
            elif item.status == 0:
                screen.blit(img_close, pos)
            elif item.status == 2:
                screen.blit(img_mine, pos)
            elif item.status == 3:
                screen.blit(img_flag, pos)
                count_flag += 1
            elif item.status == 4:
                screen.blit(img_question, pos)
            elif item.status == 5:
                screen.blit(img_boom, pos)

    if count_opened + count_flag == row * col:
        game_status = 3
        if mes == 1:
            mes = 2

    # 渲染笑脸
    if game_status == 1 or game_status == 2:
        screen.blit(img_ready, (face_pos_x, face_pos_y))
    elif game_status == 0:
        screen.blit(img_lose, (face_pos_x, face_pos_y))
    elif game_status == 3:
        screen.blit(img_win, (face_pos_x, face_pos_y))

    # 渲染时间
    if game_status == 2:
        nowtime = int(time.time() - begintime)
    drawText(screen, font, width - fwidth - 30, 0, str("%3d" % nowtime), red)

    # 渲染输入框
    rowTextSurface = font_sm.render("行", True, (0, 0, 0))
    screen.blit(rowTextSurface, (15, 8))
    rowinput.draw(screen)
    colTextSurface = font_sm.render("列", True, (0, 0, 0))
    screen.blit(colTextSurface, (70, 8))
    colinput.draw(screen)
    numTextSurface = font_sm.render("雷", True, (0, 0, 0))
    screen.blit(numTextSurface, (125, 8))
    numinput.draw(screen)
    pygame.draw.rect(screen, (240, 240, 240), submit)
    textSurface = font_sm.render("提交", True, (0, 0, 0))
    screen.blit(textSurface, (175, 22))

    pygame.display.flip()

    if mes == 2:
        messagebox.showinfo("提示", "恭喜！\n点击笑脸重新开始")
        mes = 0
    elif mes == 3:
        messagebox.showinfo("提示", "遗憾！\n点击笑脸重新开始")
        mes = 0
