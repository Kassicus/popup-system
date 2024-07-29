import pygame # this is the graphics library we will be using
import sys # this is the system library we will be using to exit the program, allows for us to pass an exit code
import datetime # allows us to get the current time for various tasks

pygame.init() # this initializes the pygame library

display_size = pygame.display.Info() # this gets the display information for the current monitor, we need it to pick font sizes for large screens

class Colors(): # this class is used to store color values for the program
    def __init__(self) -> None:

        # We define the colors we will be using in the program here, this gives us simple color.name access to the colors

        self.black = pygame.Color(0, 0, 0, 255)
        self.white = pygame.Color(255, 255, 255, 255)
        self.nexus_blue = pygame.Color(0, 153, 216, 255)
        self.nexus_light_gray = pygame.Color(237, 237, 238, 255)
        self.nexus_middle_gray = pygame.Color(119, 131, 144, 255)
        self.nexus_dark_gray = pygame.Color(80, 79, 81, 255)
        self.nexus_orange = pygame.Color(241, 138, 0, 255)
        self.nexus_green = pygame.Color(149, 201, 61, 255)

color = Colors() # we create an instance of the Colors class so we can use the color.name syntax to access the colors (see above)

class Fonts(): # this class is used to store font objects for the program
    def __init__(self) -> None:

        # We define the fonts we will be using in the program here, this gives us simple font.name access to the fonts

        self.header_font = self.configure_fonts()[0] # call the configure_fonts method to get the correct font size for our screen
        self.body_font = self.configure_fonts()[1] # call the configure_fonts method to get the correct font size for our screen

    def configure_fonts(self) -> list[pygame.font.Font, pygame.font.Font]: # this method is used to get the correct font size for our screen, it specifically returns a list with two font elements
        if display_size.current_w > 1920: # if the screen width is greater than 1920 pixels, we return a larger font size (this is mostly for 4k screens) TODO: test this further
            return[pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 48), pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 22)]
        else:
            return[pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 48), pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 20)]

font = Fonts() # we create an instance of the Fonts class so we can use the font.name syntax to access the fonts (see above)

class Images(): # this class is used to store image objects for the program
    def __init__(self) -> None:

        # We define the images we will be using in the program here, this gives us simple image.name access to the images

        self.nexus_logo = None # setting this to none so we can load later (to bypass the issue of loading images before the display is initialized)
        self.character_elk = None # setting this to none so we can load later (to bypass the issue of loading images before the display is initialized)

    def load_images(self) -> None: # We call this from the main window class so that the display is initialized before we load images
        self.nexus_logo = pygame.image.load("assets/images/nexus_logo.png").convert_alpha() # load the image from the assets folder and convert it to a format that pygame can use (alpha for transparency)
        self.nexus_logo = pygame.transform.scale(self.nexus_logo, (int(self.nexus_logo.get_width() / 8), int(self.nexus_logo.get_height() / 8))) # TODO: Replace the logo with an appropriately sized image, remove scaling

        self.character_elk = pygame.image.load("assets/images/character_elk.png").convert_alpha() # load the image from the assets folder and convert it to a format that pygame can use (alpha for transparency)
        self.character_elk = pygame.transform.scale(self.character_elk, (int(self.character_elk.get_width() / 15), int(self.character_elk.get_height() / 15))) # TODO: Replace the character with an appropriately sized image, remove scaling

images = Images() # we create an instance of the Images class so we can use the image.name syntax to access the images (see above)

class Sounds(): # this class is used to store sound objects for the program
    def __init__(self) -> None:

        # We define the sounds we will be using in the program here, this gives us simple sound.name access to the sounds

        self.alert = pygame.mixer.Sound("assets/sounds/alert.wav")

sound = Sounds() # we create an instance of the Sounds class so we can use the sound.name syntax to access the sounds (see above)

class JustifiedText(): # this class is used to create justified text objects for the program, this is more complicated than it needs to be but it works TODO: make this less complicated
    def __init__(self, text: str, max_width: int, space: int, font, surface) -> None:
        self.text = text # the text we want to justify
        self.max_width = max_width # the maximum width of the text before it wraps
        self.space = space # the minimum space between words
        self.font = font # the font object we want to use
        self.surface = surface # the surface we want to render the text to
        self.pos = (0, 0) # the position we want to render the text at

        self.words = self.text.split() # split the text into words
        self.lines = [] # the lines of text we will later render
        self.current_line = [] # the current line we are working on
        self.current_width = 0 # the current width of the line we are working on

        self.word_surfaces = [] # the surfaces of the words we will render, this is a list of lists with the word surface, x position, and y position

        self.word_height = self.font.size("Tg")[1] # the height of the font, we use "Tg" because it is the tallest combination of letters in the font

        self.create_lines() # call the create_lines method to create the lines of text, this is where the magic happens, this way we dont create the lines new every time we render

    def create_lines(self) -> None: # this method is used to create the lines of text
        for word in self.words: # loop through the words in the text
            word_width = self.font.size(word)[0] # get the width of the word
            if self.current_width + word_width + (len(self.current_line) - 1) * self.space <= self.max_width or not self.current_line: # if the current width plus the word width plus the space between words is less than the max width or the current line is empty
                self.current_line.append(word) # add the word to the current line
                self.current_width += word_width # add the word width to the current width
            else: # if the current width plus the word width plus the space between words is greater than the max width
                self.lines.append(self.current_line) # add the current line to the lines
                self.current_line = [word] # create a new line with the current word
                self.current_width = word_width # set the current width to the word width
        self.lines.append(self.current_line) # add the last line to the lines (this is necessary because the last line is not added in the loop due to not always being full length)

    def generate_word_surfaces(self, input_x: int, input_y: int) -> None: # this method is used to generate the word surfaces for the text
        self.pos = input_x, input_y # set the position of the text
        x, y = self.pos #TODO: fix this, its jenky but it works for now (this is the position we will render the text at, referencing self.pos wasnt working for some reason)

        for i, line in enumerate(self.lines): # loop through the lines of text
            line_width = sum(self.font.size(word)[0] for word in line) # get the total width of the line
            is_last_line = (i == len(self.lines) - 1) # check if the line is the last line
            if not is_last_line: # if the line is not the last line
                total_space_width = self.max_width - line_width # get the total space width (this is the amount of space we need to fill)
                if len(line) - 1 > 0: # if the line has more than one word
                    adjusted_space = total_space_width / (len(line) - 1) # calculate the adjusted space (this is the space we need to add between words)
                else: # if the line has only one word
                    adjusted_space = 0 # set the adjusted space to 0
            else: # if the line is the last line
                adjusted_space = self.space # set the adjusted space to the minimum space we want between words

            x = self.pos[0] # set the x position to the x position of the text
            for word in line: # loop through the words in the line
                word_surface = self.font.render(word, True, (0, 0, 0)) # create the actual word surface (this is the element we can render to the screen)
                self.word_surfaces.append([word_surface, x, y]) # add the word surface to the word surfaces list
                x += self.font.size(word)[0] + adjusted_space # increment the x position by the width of the word plus the adjusted space
            y += self.word_height # increment the y position by the height of the font

    def render(self) -> None: # this method is used to render the text to the screen
        for word_surface in self.word_surfaces: # loop through the word surfaces
            self.surface.blit(word_surface[0], (word_surface[1], word_surface[2])) # render the word surface to the screen

    def get_height(self) -> int: # this method is used to get the height of the whole text block
        return len(self.lines) * self.word_height # return the height of the text block by calculating the number of lines times the height of the font

class Button(pygame.sprite.Sprite): # this class is used to create button objects for the program
    def __init__(self, text: str, padding: int, fgcolor, bgcolor, command = None) -> None:
        pygame.sprite.Sprite.__init__(self) # initialize the sprite class, this allows us to use sprite methods, we have to do this because the buttons are sprites

        self.pos = pygame.math.Vector2(-500, -500) # the position of the button, we set it to -500, -500 so it is off screen by default

        self.padding = padding # the padding of the button (the amount of space between the text and edges of the button box)
        self.fgcolor = fgcolor # the foreground color of the button (the color of the text)
        self.bgcolor = bgcolor # the background color of the button

        self.hovered = False # the hovered state of the button, this is used to change the color of the button when the mouse is over it

        self.command = command # the command we want to run when the button is clicked

        self.text_surface = font.body_font.render(text, True, self.fgcolor) # the text surface of the button, this is the renderable text "label" for the button

        self.image = pygame.Surface([int(self.padding * 2) + self.text_surface.get_width(), int(self.padding * 2) + self.text_surface.get_height()]) # dynamically generate the size of the button based on the text size and padding
        self.image.fill((0, 0, 0)) # fill the button with black
        self.image.set_colorkey((0, 0, 0)) # set the color key of the button to black (this makes the button invisible)
        self.rect = self.image.get_rect() # get the rect of the button (this is used for collision detection)
        self.rect.topleft = self.pos # set the top left of the button to the position of the button

    def update(self) -> None: # this method is used to update the button
        self.check_hover() # call the check_hover method to check if the mouse is over the button

        if self.hovered: # if the mouse is over the button
            if pygame.mouse.get_pressed()[0]: # if the left mouse button is pressed
                self.run_command() # run the command

    def render_label(self, surface) -> None: # this method is used to render the button, text and change the cursor based on the hovered state
        if self.hovered: # if the mouse is over the button
            pygame.draw.rect(surface, color.nexus_blue, (self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())) # draw the button with the nexus blue color
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) # change the cursor to a hand
        else: # if the mouse is not over the button
            pygame.draw.rect(surface, self.bgcolor, (self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())) # draw the button with the default background color (nexus orange)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # change the cursor to an arrow (the default cursor)

        surface.blit(self.text_surface, (self.pos.x + self.padding, self.pos.y + self.padding)) # render the text surface to the screen, this is done last so that its on top of the background

    def check_hover(self) -> None: # this method is used to check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos() # get the position of the mouse

        if self.pos.x < mouse_pos[0] < self.pos.x + self.rect.width and self.pos.y < mouse_pos[1] < self.pos.y + self.rect.height: # if the mouse x and y are within the buttons rect
            self.hovered = True # set the hovered state to true
        else: # if the mouse x and y are not within the buttons rect
            self.hovered = False # set the hovered state to false

    def get_width(self) -> int: # this method is used to get the width of the button
        return self.rect.width # return the width of the button
    
    def run_command(self) -> None: # this method is used to run the command of the button
        if self.command is not None: # if the button has an assigned command
            self.command() # run the command


class Window(): # this class is used to create the main window object for the program, this is the big boy
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([800, 600], pygame.NOFRAME) # create the screen with a resolution of 800x600 and no frame (this removes the title bar and the [x] button)
        images.load_images() # load the images after the display is initialized, if we don't do this here things break

        self.running = True # the running state of the window, this is used to control the main loop
        self.events = pygame.event.get() # the events of the window, this is used to get the events that are happening in the window, useful for mouse and keyboard interaction

        self.exit_code = 0 # default exit code is 0, means successful

        self.init_time = datetime.datetime.now() # get the current time, this is used to calculate the elapsed time
        self.elapsed_time = None # the elapsed time of the window, this is used to calculate how long the window has been open, we are just initializing this for now

        self.clock = pygame.time.Clock() # create a clock object, this is used to control the frame rate of the window, it is how we cap the refresh rate to 30 fps

        self.header_text = "This Is A Test Popup!" # the header text of the window, this is the big text at the top of the window
        self.header_surface = font.header_font.render(self.header_text, True, color.white) # the header surface of the window, this is the renderable text for the header

        self.fps_text = f"{int(self.clock.get_fps())}" # the fps text of the window, this is the text that displays the current frames per second
        self.fps_surface = None # the fps surface of the window, simply initializing this for now
        self.render_fps = False # the render fps state of the window, this is used to control if we render the fps text to the screen

        self.text_1 = "PLEASE READ: " # first block of text we want to display
        self.text_2 = "This Popup is just for testing" # second block of text we want to display
        self.text_3 = "This is a long line of filler text to test out the auto justify tool and verify that when I make changes to the codebase, the justify tool will still work as intended." # third block of text we want to display

        self.body_text = [self.text_1, self.text_2, self.text_3] # this is not used yet, TODO: automate the process of creating the justified text blocks based on quantity 

        self.cancel_button = Button("Press Me To Close The Popup!", 25, color.white, color.nexus_orange, self.close) # this is the button that closes the window (see button class above)
        self.cancel_button.pos = pygame.math.Vector2(int(400 - (self.cancel_button.get_width() / 2)), 475) # set the position of the button to the center of the screen near the bottom

        self.justified_text_1 = JustifiedText(self.text_1, 400, 10, font.body_font, self.screen) # create the justified text object for the first block of text
        self.justified_text_2 = JustifiedText(self.text_2, 400, 10, font.body_font, self.screen) # create the justified text object for the second block of text
        self.justified_text_3 = JustifiedText(self.text_3, 400, 10, font.body_font, self.screen) # create the justified text object for the third block of text

        self.justified_text_1.generate_word_surfaces(200, 70 + self.header_surface.get_height() + 35) # generate the word surfaces for the first block of text
        self.justified_text_2.generate_word_surfaces(200, self.justified_text_1.pos[1] + self.justified_text_1.get_height() + 35) # generate the word surfaces for the second block of text
        self.justified_text_3.generate_word_surfaces(200, self.justified_text_2.pos[1] + self.justified_text_2.get_height() + 35) # generate the word surfaces for the third block of text

        self.buttons = pygame.sprite.Group() # create a sprite group for the buttons (this allows us to manage multiple buttons at once)
        self.buttons.add(self.cancel_button) # add the cancel button to the buttons group (we can add more buttons later if we want)

        #sound.alert.play() # play the alert sound when the window is created

    def start(self) -> None: # this method is used to start the main loop of the window
        while self.running: # while the window is running
            self.event_loop() # call the event loop method
            self.update() # call the update method
            self.draw() # call the draw method
 
    def event_loop(self) -> None: # this method is used to handle the events of the window
        self.events = pygame.event.get() # get the events of the window (refreshing this every time we need to run events)

        for event in self.events: # loop through the events
            if event.type == pygame.QUIT: # if the event is a quit event
                self.close() # call the close method, ending the program

            if event.type == pygame.KEYDOWN: # if the event is a key down event
                if event.key == pygame.K_q: # if the key is the q key
                    self.close() # call the close method, ending the program

                if event.key == pygame.K_f: # if the key is the f key
                    self.render_fps = not self.render_fps # toggle the render fps state

                if event.key == pygame.K_e: # if the key is the e key
                    self.close_with_error(error = "manufactured error", code = 69) # close the window with an error (and some dumb code)

    def close(self) -> None: # this method is used to close the window
        print(self.elapsed_time) # print the elapsed time when the window is closed (total amount of time the program has ran)
        self.running = False # set the running state to false, this ends the main loop

    def close_with_error(self, error: str = "", code: int = 1) -> None: # this method is used to close the window with an error, message and code are customizable
        print(f"An error occurred: {error}") # print the error message when the window is closed
        self.exit_code = code # set the exit code to the code provided
        self.close() # call the close method, ending the program

    def update(self) -> None: # this method is used to do all of the logic
        self.buttons.update() # update the buttons

        self.elapsed_time = datetime.datetime.now() - self.init_time # calculate the elapsed time

        #if int(self.elapsed_time.total_seconds()) % 60 == 0: # every 60 seconds
            #sound.alert.play() # play the alert sound
            
        pygame.display.update() # update the display (doing this here for stupid pygame reasons)
        self.clock.tick(30) # cap the frame rate to 30 fps and process the tick

    def draw(self) -> None: # this method is used to draw everything to the screen
        self.screen.fill(color.white) # fill the screen with white (this is the background color)
        pygame.draw.rect(self.screen, color.nexus_blue, (0, 0, 800, 35 + int(self.header_surface.get_height() + 35))) # draw the header background (the nexus blue banner)

        self.screen.blit(self.header_surface, (400 - (self.header_surface.get_width() / 2), 35)) # render the header text to the screen

        self.screen.blit(images.character_elk, (-75, 600 - images.character_elk.get_height() - 10)) # render the character to the screen (this way its behind any elements that need to be read)
        
        # TODO: link this to the automatic creation and rendering of justified text blocks
        self.justified_text_1.render() # render the justified text for the first block of text
        self.justified_text_2.render() # render the justified text for the second block of text
        self.justified_text_3.render() # render the justified text for the third block of text

        self.buttons.draw(self.screen) # draw the buttons to the screen

        for button in self.buttons: # loop through the buttons
            button.render_label(self.screen) # render the button labels to the screen (this is done in a loop so each button can have different hover functionality)

        if self.render_fps: # if the render fps state is true
            self.fps_text = f"{int(self.clock.get_fps())}" # update the fps text to the current frames per second
            self.fps_surface = font.body_font.render(self.fps_text, True, color.nexus_orange) #  generate the renderable surface for the fps text
            self.screen.blit(self.fps_surface, (800 - self.fps_surface.get_width() - 10, 600 - self.fps_surface.get_height() - 10)) # render the fps text to the screen

if __name__ == '__main__': # this is the main entry point of the program
    win = Window() # create an instance of the Window class
    win.start() # call the start method of the Window class (starting the program main loop)
    sys.exit(win.exit_code) # exit the program with the exit code provided by the window class (just because the window stops running does not mean the object ceases to exist, so we reference the stop code here)