import pygame

pygame.init()

colors = {
    "black": pygame.Color(0, 0, 0, 255),
    "white": pygame.Color(255, 255, 255, 255),
    "red": pygame.Color(255, 0, 0, 255)
}

class Square(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pygame.math.Vector2(100, 100)

        self.image = pygame.Surface([50, 50])
        self.image.fill(colors["red"])
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

class Window():
    def __init__(self):
        self.screen = pygame.display.set_mode([800, 600], pygame.NOFRAME)
        pygame.display.set_caption("System Uptime Notice")

        self.running = True
        self.events = pygame.event.get()
        self.header_font = pygame.font.SysFont("Roboto", 24)

        self.header_text = "System Uptime Notice"

        self.header_surface = self.header_font.render(self.header_text, True, colors["white"])

        self.test_square = Square()

        self.content = pygame.sprite.Group()
        self.content.add(self.test_square)

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

    def update(self):
        self.content.update()

    def draw(self):
        self.screen.fill(colors["white"])
        self.screen.blit(self.header_surface, (100, 100))
        self.content.draw(self.screen)

if __name__ == '__main__':
    win = Window()
    win.start()
    pygame.quit()