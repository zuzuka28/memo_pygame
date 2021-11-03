import pygame
import random

from button import button


class memo_game:
    def __init__(self, screen):
        self.BOARDWIDTH = 2  # количество столбцов в игре
        self.BOARDHEIGHT = 2  # количество строк в игре

        self.screen = screen

        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        self.SPEEDDEMONSTRATION = 2
        self.BOXSIZE = 80  # размер карточек
        self.GAPSIZE = 20  # отступы между карточками

        self.XMARGIN = int((self.WIDTH - (self.BOARDWIDTH * (self.BOXSIZE + self.GAPSIZE))) / 2)
        self.YMARGIN = int((self.HEIGHT - (self.BOARDHEIGHT * (self.BOXSIZE + self.GAPSIZE))) / 2)

        # радуга палитра
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 128, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.CYAN = (0, 255, 255)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (255, 0, 255)
        self.GRAY = (100, 100, 100)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # возможные фигуры
        self.CIRCLE = 'circle'
        self.SQUARE = 'square'
        self.DIAMOND = 'diamond'
        self.LINES = 'lines'
        self.OVAL = 'oval'

        # цвета и формы
        self.ALLCOLORS = (self.RED, self.GREEN, self.BLUE, self.YELLOW, self.ORANGE, self.PURPLE, self.CYAN)
        self.ALLSHAPES = (self.CIRCLE, self.SQUARE, self.DIAMOND, self.LINES, self.OVAL)

        self.mainBoard = self.getRandomizedBoard()
        self.revealedBoxes = self.generateRevealedBoxesData(False)
        self.firstSelection = None

        self.is_start = True
        self.return_button = button("res/button_blue.png")
        self.return_button.add_button((49, 48), (339, 95, 388, 143), '', (255, 255, 255))
        self.return_button.add_button((49, 45), (290, 95, 340, 140), '', (255, 255, 255))
        self.return_button.set_picture('res/icons.png', (4 * 51 - 5, 51 + 5, 5 * 51 - 5, 2 * 51 + 5), (40, 40))
        self.return_button.draw_button(self.screen, 0, (1500, 700))

    def draw_button(self, is_clicked, pos):
        if is_clicked and self.return_button.check_pos_in_button(pos):
            self.return_button.draw_button(self.screen, 1, (1500, 700))
            self.is_start = True
            self.mainBoard = self.getRandomizedBoard()
            self.revealedBoxes = self.generateRevealedBoxesData(False)
            return 0
        else:
            self.return_button.draw_button(self.screen, 0, (1500, 700))
            return 3

    def getRandomizedBoard(self):
        # создание случайного набора возможных комбинаций форм и цветов

        icons = []
        for color in self.ALLCOLORS:
            for shape in self.ALLSHAPES:
                icons.append((shape, color))
        random.shuffle(icons)

        # создание нужного количества пар и перемешивание их

        numIconsUsed = int(self.BOARDWIDTH * self.BOARDHEIGHT / 2)
        icons = icons[:numIconsUsed] * 2
        random.shuffle(icons)

        # создание доски
        # при этом список иконок сокращаем

        board = []
        for x in range(self.BOARDWIDTH):
            column = []
            for y in range(self.BOARDHEIGHT):
                column.append(icons[0])
                del icons[0]
            board.append(column)

        return board

    def generateRevealedBoxesData(self, val):
        # cоздание списка еще скрытых карточек
        revealedBoxes = []
        for i in range(self.BOARDWIDTH):
            revealedBoxes.append([val] * self.BOARDHEIGHT)
        return revealedBoxes

    def boxPos(self, boxx, boxy):
        # преобразование координат доски в пиксельные координаты

        bX = boxx * (self.BOXSIZE + self.GAPSIZE) + self.XMARGIN
        bY = boxy * (self.BOXSIZE + self.GAPSIZE) + self.YMARGIN

        return (bX, bY)

    def getBoxAtPixel(self, x, y):
        # проверка наличия карточки на месте крысы

        for boxx in range(self.BOARDWIDTH):
            for boxy in range(self.BOARDHEIGHT):
                boxRect = pygame.Rect(self.boxPos(boxx, boxy)[0], self.boxPos(boxx, boxy)[1], self.BOXSIZE,
                                      self.BOXSIZE)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)

        return (None, None)

    def drawIcon(self, shape, color, boxx, boxy):
        # отрисовываем фигурки

        if shape == self.CIRCLE:
            pygame.draw.circle(self.screen, color,
                               (self.boxPos(boxx, boxy)[0] + int(self.BOXSIZE * 0.5),
                                self.boxPos(boxx, boxy)[1] + int(self.BOXSIZE * 0.5)),
                               int(self.BOXSIZE * 0.5) - 5)

        elif shape == self.SQUARE:
            pygame.draw.rect(self.screen, color, (
                self.boxPos(boxx, boxy)[0] + int(self.BOXSIZE * 0.25),
                self.boxPos(boxx, boxy)[1] + int(self.BOXSIZE * 0.25),
                self.BOXSIZE - int(self.BOXSIZE * 0.5), self.BOXSIZE - int(self.BOXSIZE * 0.5)))

        elif shape == self.DIAMOND:
            pygame.draw.polygon(self.screen, color, (
                (self.boxPos(boxx, boxy)[0] + int(self.BOXSIZE * 0.5), self.boxPos(boxx, boxy)[1]),
                (self.boxPos(boxx, boxy)[0] + self.BOXSIZE - 1, self.boxPos(boxx, boxy)[1] + int(self.BOXSIZE * 0.5)),
                (self.boxPos(boxx, boxy)[0] + int(self.BOXSIZE * 0.5), self.boxPos(boxx, boxy)[1] + self.BOXSIZE - 1),
                (self.boxPos(boxx, boxy)[0], self.boxPos(boxx, boxy)[1] + int(self.BOXSIZE * 0.5))))

        elif shape == self.LINES:
            for i in range(0, self.BOXSIZE, 4):
                pygame.draw.line(self.screen, color, (self.boxPos(boxx, boxy)[0], self.boxPos(boxx, boxy)[1] + i),
                                 (self.boxPos(boxx, boxy)[0] + i, self.boxPos(boxx, boxy)[1]))
                pygame.draw.line(self.screen, color,
                                 (self.boxPos(boxx, boxy)[0] + i, self.boxPos(boxx, boxy)[1] + self.BOXSIZE - 1),
                                 (self.boxPos(boxx, boxy)[0] + self.BOXSIZE - 1, self.boxPos(boxx, boxy)[1] + i))

        elif shape == self.OVAL:
            pygame.draw.ellipse(self.screen, color, (
                self.boxPos(boxx, boxy)[0], self.boxPos(boxx, boxy)[1] + int(self.BOXSIZE * 0.25), self.BOXSIZE,
                int(self.BOXSIZE * 0.5)))

    def getShapeAndColor(self, board, boxx, boxy):
        # получаем форму board[boxx][boxy][0]
        # получаем цвет board[boxx][boxy][1]

        return board[boxx][boxy][0], board[boxx][boxy][1]

    def drawBoxCovers(self, board, boxes, coverage):
        # список карточек для отрисовки
        # отражает закрашенные и не закрашенные
        clock = pygame.time.Clock()
        for box in boxes:
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (self.boxPos(box[0], box[1])[0], self.boxPos(box[0], box[1])[1], self.BOXSIZE,
                              self.BOXSIZE))
            shape, color = self.getShapeAndColor(board, box[0], box[1])
            self.drawIcon(shape, color, box[0], box[1])

            if coverage > 0:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (self.boxPos(box[0], box[1])[0], self.boxPos(box[0], box[1])[1], coverage,
                                  self.BOXSIZE))
        pygame.display.flip()
        clock.tick(60)

    def showBoxes(self, board, boxesToShow):
        # показывает карточки перед игрой

        for coverage in range(self.BOXSIZE, (-self.SPEEDDEMONSTRATION) - 1, - self.SPEEDDEMONSTRATION):
            self.drawBoxCovers(board, boxesToShow, coverage)
        for coverage in range(0, self.BOXSIZE + self.SPEEDDEMONSTRATION, self.SPEEDDEMONSTRATION):
            self.drawBoxCovers(board, boxesToShow, coverage)

    def openBoxAnim(self, board, boxesToReveal):
        # открытие карточки

        for coverage in range(self.BOXSIZE, (-self.SPEEDDEMONSTRATION) - 1, - self.SPEEDDEMONSTRATION):
            self.drawBoxCovers(board, boxesToReveal, coverage)

    def closeBoxAnim(self, board, boxesToCover):
        # закрытие карточки

        for coverage in range(0, self.BOXSIZE + self.SPEEDDEMONSTRATION, self.SPEEDDEMONSTRATION):
            self.drawBoxCovers(board, boxesToCover, coverage)

    def drawBoard(self, board, revealed):
        # отрисовка доски и карточек в обоих состояниях

        for boxx in range(self.BOARDWIDTH):
            for boxy in range(self.BOARDHEIGHT):
                if not revealed[boxx][boxy]:
                    # отрисовка закрытой карточки

                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (self.boxPos(boxx, boxy)[0], self.boxPos(boxx, boxy)[1], self.BOXSIZE,
                                      self.BOXSIZE))

                else:

                    # отрисовка открытой карточки

                    shape, color = self.getShapeAndColor(board, boxx, boxy)
                    self.drawIcon(shape, color, boxx, boxy)

    def startGame(self, board):
        # первоначальная отрисовка всего

        coveredBoxes = self.generateRevealedBoxesData(False)
        boxes = []
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                boxes.append((x, y))
        random.shuffle(boxes)
        self.drawBoard(board, coveredBoxes)
        self.showBoxes(board, boxes)

    def hasWon(self, revealedBoxes):
        # проверка на выигрыш

        for i in revealedBoxes:
            if False in i:
                return False
        return True

    def update(self, is_clicked, pos):
        self.screen.fill((0, 0, 0))
        if self.is_start:
            self.startGame(self.mainBoard)
            self.is_start = False
            return 3
        self.drawBoard(self.mainBoard, self.revealedBoxes)

        boxx, boxy = self.getBoxAtPixel(pos[0], pos[1])
        if boxx is not None and boxy is not None:
            # получение клика по карточке и его обработка

            # если это закрытая карточка

            if not self.revealedBoxes[boxx][boxy] and is_clicked:
                self.openBoxAnim(self.mainBoard, [(boxx, boxy)])
                self.revealedBoxes[boxx][boxy] = True

                # выбор первой карты

                if self.firstSelection is None:
                    self.firstSelection = (boxx, boxy)

                else:

                    icon1shape, icon1color = self.getShapeAndColor(self.mainBoard, self.firstSelection[0],
                                                                   self.firstSelection[1])
                    icon2shape, icon2color = self.getShapeAndColor(self.mainBoard, boxx, boxy)

                    # если не совпадают

                    if icon1shape != icon2shape or icon1color != icon2color:

                        pygame.time.wait(500)
                        self.closeBoxAnim(self.mainBoard,
                                          [(self.firstSelection[0], self.firstSelection[1]), (boxx, boxy)])
                        self.revealedBoxes[self.firstSelection[0]][self.firstSelection[1]] = False
                        self.revealedBoxes[boxx][boxy] = False

                    elif self.hasWon(self.revealedBoxes):
                        # сброс всего при выигрыше
                        self.BOARDWIDTH += 2
                        self.BOARDHEIGHT += 1

                        self.mainBoard = self.getRandomizedBoard()
                        self.revealedBoxes = self.generateRevealedBoxesData(False)
                        self.drawBoard(self.mainBoard, self.revealedBoxes)

                        pygame.time.wait(1000)
                        self.startGame(self.mainBoard)

                    self.firstSelection = None
        return self.draw_button(is_clicked, pos)
