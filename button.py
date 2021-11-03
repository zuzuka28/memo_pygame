import pygame


class button(object):
    def __init__(self, image_path):
        self.images = []
        self.png = pygame.image.load(image_path)
        self.font = pygame.font.SysFont('Corbel', 25)
        self.texts = []
        self.pos = []
        self.cur_im_ind = 0
        self.is_picture = False

    def image_at(self, image_size, image_pos, colorkey=None):
        rect = pygame.Rect(image_pos)
        image = pygame.Surface(image_size).convert()
        image.blit(self.png, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def draw_button(self, screen, i, pos):
        screen.blit(self.images[i],
                    (pos[0] - self.images[i].get_width() // 2, pos[1] - self.images[i].get_height() // 2))
        if not self.is_picture:
            t = self.font.render(self.texts[i][0], True, self.texts[i][1])
            screen.blit(t, (pos[0] - t.get_width() // 2, pos[1] - t.get_height() // 2))
        else:
            screen.blit(self.icon, (pos[0] - self.icon.get_width() // 2, pos[1] - self.icon.get_height() // 2))
        self.pos = pos
        self.cur_im_ind = i

    def add_button(self, image_size, image_pos, text, text_color=(50, 50, 50)):
        self.images.append(self.image_at(image_size, image_pos, (0, 0, 0)))
        self.texts.append((text, text_color))

    def check_pos_in_button(self, pos):
        if (self.pos[0] - self.images[self.cur_im_ind].get_width() // 2 <= pos[0] <= self.pos[0] +
                self.images[self.cur_im_ind].get_width() // 2 and self.pos[1] - self.images[
                    self.cur_im_ind].get_height() // 2 <= pos[1] <= self.pos[1] + self.images[
                    self.cur_im_ind].get_height() // 2):
            return True
        else:
            return False

    def set_picture(self, path, rect, pic_size):
        self.is_picture = True
        sheet = pygame.image.load(path)
        r = pygame.Rect(rect)
        size = (rect[2] - rect[0], rect[3] - rect[1])
        image = pygame.Surface(size).convert()
        image.blit(sheet, (0, 0), rect)
        image = pygame.transform.scale(image, pic_size)
        image.set_colorkey((0, 0, 0))
        self.icon = image

    def scale_tex(self, ind, size):
        self.images[ind] = pygame.transform.scale(self.images[ind], (size[0], size[1]))

    def set_text(self, text, text_color=(50, 50, 50)):
        self.texts.clear()
        self.texts.append((text, text_color))
        self.texts.append((text, text_color))
