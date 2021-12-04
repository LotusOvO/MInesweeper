import pygame


class InputBox:
    def __init__(self, length, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32)) -> None:
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')  # 未被选中的颜色
        self.color_active = pygame.Color('dodgerblue2')  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = ''
        self.done = False
        self.length = length
        self.font = pygame.font.Font("./resources/simhei.ttf", 32)

    def dealEvent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.boxBody.collidepoint(event.pos):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if (
                self.active) else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.length:
                        self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        txtSurface = self.font.render(
            self.text, True, (0, 0, 0))
        width = 16 * self.length
        self.boxBody.w = width
        screen.blit(txtSurface, (self.boxBody.x + 4, self.boxBody.y + 3))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)
