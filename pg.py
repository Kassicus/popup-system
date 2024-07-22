import pygame

pygame.init()

colors = {
    "black": pygame.Color(0, 0, 0, 255),
    "white": pygame.Color(255, 255, 255, 255),
    "nexus_blue": pygame.Color(0, 153, 216, 255),
    "nexus_light_gray": pygame.Color(237, 237, 238, 255),
    "nexus_middle_gray": pygame.Color(119, 131, 144, 255),
    "nexus_dark_gray": pygame.Color(80, 79, 81, 255),
    "nexus_orange": pygame.Color(241, 138, 0, 255),
    "nexus_green": pygame.Color(149, 201, 61, 255)
}

fonts = {
    "header_font": pygame.font.SysFont("Roboto", 48, True),
    "body_font": pygame.font.SysFont("Roboto", 24)
}


def blit_text(surface, text, pos, font, color = colors["black"], max_width = 400, max_height = 400):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = max_width, max_height
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


class Button(pygame.sprite.Sprite):
    def __init__(self, text: str, padding: int, fgcolor, bgcolor, command = None):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pygame.math.Vector2(-500, -500)

        self.padding = padding
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor

        self.hovered = False

        self.command = command

        self.text_surface = fonts["body_font"].render(text, True, self.fgcolor)

        self.image = pygame.Surface([int(self.padding * 2) + self.text_surface.get_width(), int(self.padding * 2) + self.text_surface.get_height()])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self):
        self.check_hover()

        if self.hovered:
            if pygame.mouse.get_pressed()[0]:
                self.run_command()

    def render_label(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, colors["nexus_blue"], (self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height()))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.draw.rect(surface, self.bgcolor, (self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height()))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        surface.blit(self.text_surface, (self.pos.x + self.padding, self.pos.y + self.padding))

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.pos.x < mouse_pos[0] < self.pos.x + self.rect.width and self.pos.y < mouse_pos[1] < self.pos.y + self.rect.height:
            self.hovered = True
        else:
            self.hovered = False

    def get_width(self):
        return self.rect.width
    
    def run_command(self):
        if self.command is not None:
            self.command()


class Window():
    def __init__(self):
        self.screen = pygame.display.set_mode([800, 600], pygame.NOFRAME)
        #pygame.display.set_caption("System Uptime Notice")

        self.running = True
        self.events = pygame.event.get()
        
        self.header_text = "System Uptime Notice"
        self.header_surface = fonts["header_font"].render(self.header_text, True, colors["white"])

        self.body_text = "This is just a warning that your system uptime has exceeded 24 hours. If your system uptime exceeds 7 days you will be required to reboot. We recommend saving and closing all programs and running any available windows updates followed by a reboot at your earliest convienience."

        #self.ok_button = Button(100, 500, "Ok", 25, colors["white"], colors["nexus_green"])
        self.cancel_button = Button("Acknowledge", 25, colors["white"], colors["nexus_orange"], self.close)
        self.cancel_button.pos = pygame.math.Vector2(int(400 - (self.cancel_button.get_width() / 2)), 475)

        self.buttons = pygame.sprite.Group()
        #self.buttons.add(self.ok_button)
        self.buttons.add(self.cancel_button)

    def start(self):
        while self.running:
            self.event_loop()
            self.update()
            self.draw()

    def event_loop(self):
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

    def close(self):
        self.running = False

    def update(self):
        pygame.display.update()
        self.buttons.update()

    def draw(self):
        self.screen.fill(colors["white"])
        pygame.draw.rect(self.screen, colors["nexus_blue"], (0, 0, 800, 35 + int(self.header_surface.get_height() + 35)))
        
        self.screen.blit(self.header_surface, (400 - int(self.header_surface.get_width() / 2), 35))
        blit_text(self.screen, self.body_text, (50, 225), fonts["body_font"], max_width = 750)

        self.buttons.draw(self.screen)

        for button in self.buttons:
            button.render_label(self.screen)


if __name__ == '__main__':
    win = Window()
    win.start()
    pygame.quit()