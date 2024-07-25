import pygame
import sys
import datetime

pygame.init()

display_size = pygame.display.Info()

class Colors():
    def __init__(self):
        self.black = pygame.Color(0, 0, 0, 255)
        self.white = pygame.Color(255, 255, 255, 255)
        self.nexus_blue = pygame.Color(0, 153, 216, 255)
        self.nexus_light_gray = pygame.Color(237, 237, 238, 255)
        self.nexus_middle_gray = pygame.Color(119, 131, 144, 255)
        self.nexus_dark_gray = pygame.Color(80, 79, 81, 255)
        self.nexus_orange = pygame.Color(241, 138, 0, 255)
        self.nexus_green = pygame.Color(149, 201, 61, 255)

color = Colors()

class Fonts():
    def __init__(self):
        self.header_font = None
        self.body_font = None

        self.configure_fonts()

    def configure_fonts(self):
        if display_size.current_w > 1920:
            self.header_font = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 48)
            self.body_font = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 22)
        else:
            self.header_font = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 48)
            self.body_font = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 20)

font = Fonts()

class Images():
    def __init__(self):
        self.nexus_logo = None

        self.scale = 8

    def load_images(self):
        self.nexus_logo = pygame.image.load("assets/images/nexus_logo.png").convert_alpha()
        self.nexus_logo = pygame.transform.scale(self.nexus_logo, (int(self.nexus_logo.get_width() / self.scale), int(self.nexus_logo.get_height() / self.scale)))

images = Images()

class Sounds():
    def __init__(self):
        self.test = pygame.mixer.Sound("assets/sounds/test.wav")

sound = Sounds()

class JustifiedText():
    def __init__(self, text: str, max_width: int, space: int, font, surface):
        self.text = text
        self.max_width = max_width
        self.space = space
        self.font = font
        self.surface = surface
        self.pos = (0, 0)

        self.words = self.text.split()
        self.lines = []
        self.current_line = []
        self.current_width = 0

        self.word_height = self.font.size("Tg")[1]

        self.create_lines()

    def create_lines(self):
        for word in self.words:
            word_width = self.font.size(word)[0]
            if self.current_width + word_width + (len(self.current_line) - 1) * self.space <= self.max_width or not self.current_line:
                self.current_line.append(word)
                self.current_width += word_width
            else:
                self.lines.append(self.current_line)
                self.current_line = [word]
                self.current_width = word_width
        self.lines.append(self.current_line)

    def render(self, input_x: int, input_y: int):
        self.pos = input_x, input_y
        x, y = self.pos #TODO: fix this, its jenky but it works for now

        for i, line in enumerate(self.lines):
            line_width = sum(self.font.size(word)[0] for word in line)
            is_last_line = (i == len(self.lines) - 1)
            if not is_last_line:
                total_space_width = self.max_width - line_width
                if len(line) - 1 > 0:
                    adjusted_space = total_space_width / (len(line) - 1)
                else:
                    adjusted_space = 0
            else:
                adjusted_space = self.space

            x = self.pos[0]
            for word in line:
                word_surface = self.font.render(word, True, (0, 0, 0))
                self.surface.blit(word_surface, (x, y))
                x += self.font.size(word)[0] + adjusted_space
            y += self.word_height

    def get_height(self):
        return len(self.lines) * self.word_height

class Button(pygame.sprite.Sprite):
    def __init__(self, text: str, padding: int, fgcolor, bgcolor, command = None):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pygame.math.Vector2(-500, -500)

        self.padding = padding
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor

        self.hovered = False

        self.command = command

        self.text_surface = font.body_font.render(text, True, self.fgcolor)

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
            pygame.draw.rect(surface, color.nexus_blue, (self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height()))
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
        images.load_images()

        self.running = True
        self.events = pygame.event.get()

        self.init_time = datetime.datetime.now()
        self.elapsed_time = None

        self.clock = pygame.time.Clock()

        self.header_text = "This Is A Test Popup!"
        self.header_surface = font.header_font.render(self.header_text, True, color.nexus_blue)

        self.fps_text = f"{int(self.clock.get_fps())}"
        self.fps_surface = None
        self.render_fps = False

        self.text_1 = "PLEASE READ: "
        self.text_2 = "This Popup is just for testing"
        self.text_3 = "This is a long line of filler text to test out the auto justify tool and verify that when I make changes to the codebase, the justify tool will still work as intended."

        self.body_text = [self.text_1, self.text_2]

        self.cancel_button = Button("Press Me To Close The Popup!", 25, color.white, color.nexus_orange, self.close)
        self.cancel_button.pos = pygame.math.Vector2(int(400 - (self.cancel_button.get_width() / 2)), 475)

        self.justified_text_1 = JustifiedText(self.text_1, 700, 10, font.body_font, self.screen)
        self.justified_text_2 = JustifiedText(self.text_2, 700, 10, font.body_font, self.screen)
        self.justified_text_3 = JustifiedText(self.text_3, 700, 10, font.body_font, self.screen)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.cancel_button)

        #sound.test.play()

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

                if event.key == pygame.K_f:
                    self.render_fps = not self.render_fps

    def close(self):
        print(self.elapsed_time)
        self.running = False

    def update(self):
        self.buttons.update()

        self.elapsed_time = datetime.datetime.now() - self.init_time

        pygame.display.update()
        self.clock.tick()

    def draw(self):
        self.screen.fill(color.white)
        #pygame.draw.rect(self.screen, color.nexus_blue, (0, 0, 800, 35 + int(self.header_surface.get_height() + 35)))
        
        self.screen.blit(images.nexus_logo, (50, 35))

        self.screen.blit(self.header_surface, (50 + images.nexus_logo.get_width() + 25, 50))
        
        self.justified_text_1.render(50, 70 + self.header_surface.get_height() + 35)
        self.justified_text_2.render(50, self.justified_text_1.pos[1] + self.justified_text_1.get_height() + 35)
        self.justified_text_3.render(50, self.justified_text_2.pos[1] + self.justified_text_2.get_height() + 35)

        self.buttons.draw(self.screen)

        for button in self.buttons:
            button.render_label(self.screen)

        if self.render_fps:
            self.fps_text = f"{int(self.clock.get_fps())}"
            self.fps_surface = font.body_font.render(self.fps_text, True, color.nexus_orange)
            self.screen.blit(self.fps_surface, (800 - self.fps_surface.get_width() - 10, 600 - self.fps_surface.get_height() - 10))

if __name__ == '__main__':
    win = Window()
    win.start()
    sys.exit(0)