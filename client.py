import pygame
from network import Network

pygame.font.init()

width = 630
height = 630
add = 40
win = pygame.display.set_mode((width, height + add))
pygame.display.set_caption("Client")

bg = pygame.image.load("chocolate.png")
bg = pygame.transform.scale(bg, (630, 630))
ch = pygame.image.load("back.png")


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def buttons(i, j):
    text = str(i) + ',' + str(j)
    i = 105 * i
    j = 105 * j
    return Button(text, i, j)


def cut(win, x, y):
    pygame.draw.rect(win, (255, 235, 205), (x * 105, 0, 630, (y + 1) * 105))


def redrawWindow(win, game, p):
    global btns

    if game.get_last() != -1:

        move = game.get_player_move(game.get_last())
        cut(win, int(move[0]), int(move[2]))
        btns = [btns[i] for i in range(len(btns)) if (int(btns[i].text[0]) < int(move[0]) or
                                                      int(btns[i].text[2]) > int(move[2]))]
        pygame.draw.rect(win, (255, 235, 205), (0, 630, 630, 670))

        if p == game.get_last():
            font = pygame.font.SysFont(pygame.font.get_fonts()[28], 30)
            text = font.render("Wait!", 1, (255, 0, 0))
            win.blit(text, (300, 630))
        else:
            font = pygame.font.SysFont(pygame.font.get_fonts()[28], 30)
            text = font.render("Go!", 1, (255, 0, 0))
            win.blit(text, (300, 630))

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    win.blit(bg, (0, 0))
    global btns
    btns = []
    for i in range(6):
        for j in range(6):
            btns.append(buttons(i, j))

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.get_end():

            font = pygame.font.SysFont(pygame.font.get_fonts()[79], 70)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255, 0, 0))

            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(1000)

            connecting()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if game.get_last() != 0:
                                n.send(btn.text)
                        else:
                            if game.get_last() != 1:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def connecting():
    run = True
    clock = pygame.time.Clock()
    n = Network()

    while run:
        clock.tick(60)
        win.fill((255, 235, 205))

        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        if not (game.connected()):
            font = pygame.font.get_fonts()[28]
            win.fill((255, 235, 205))
            win.blit(ch, (50, 280))
            font = pygame.font.SysFont(font, 40)
            text = font.render("Waiting for player...", 1, (255, 0, 0))
            win.blit(text, (100, 200))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        else:
            run = False

    main()


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        font = pygame.font.get_fonts()[28]
        win.fill((255, 235, 205))
        win.blit(ch, (50, 280))
        font = pygame.font.SysFont(font, 50)
        text = font.render("Click to play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    connecting()


while True:
    menu_screen()
