import pygame
import gui.buttons as buttons
import threading
"""
pygame used for gui
# buttons is my own library
threading library used for creating timer for enabling and disabling buttons
lines: 52 - 53

Overriding of __new__ method used from Stackoverflow.
Lines: 20 - 23
https://stackoverflow.com/a/1810367

"""
pygame.init()


class Menu:
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls, screen):   # method used to ensure only one object is created
        if cls._instance is None:   # If an instance does not exist, a new one will be created
            cls._instance = super(Menu, cls).__new__(cls)
        return cls._instance    # If an instance already exists, it will be returned and used.

    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        #   Get screen dimensions
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w , info.current_h

        #   Create Game window
        self.screen = screen

        pygame.display.set_caption("Menu")

        # Load and scale background image
        self.background_image = pygame.image.load('resources/images/buttons/MenuBackground.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        # Load and scale menu title image
        self.menu_title = pygame.image.load('resources/images/buttons/title.png').convert_alpha()
        self.menu_title = pygame.transform.scale(self.menu_title, (self.WIDTH * 0.321, self.HEIGHT * 0.178))

        # Create buttons
        button_names = ['StartButton.png', 'DataButton.png', 'AnalyseButton.png', 'TheoryButton.png',
                        'QuitButton.png']
        image_paths = ['resources/images/buttons/' + i for i in button_names]
        images = self.load_button_images(image_paths, 1)  # Load all images in list

        self.start_button = buttons.Button(0.4, 0.309, 0.1875, 0.1065, images[0], self.WIDTH, self.HEIGHT)

        #   Short Delay to prevent miss clicks
        self.start_button.DisableAll()
        threading.Timer(0.5, self.start_button.EnableAll).start()

        self.data_button = buttons.Button(0.4, 0.4467, 0.1875, 0.1065, images[1], self.WIDTH, self.HEIGHT)
        self.analyse_button = buttons.Button(0.4, 0.584, 0.1875, 0.1065, images[2], self.WIDTH, self.HEIGHT)
        self.theory_button = buttons.Button(0.4, 0.722, 0.1875, 0.1065, images[3], self.WIDTH, self.HEIGHT)
        self.quit_button = buttons.Button(0.02, 0.822, 0.1875, 0.1065, images[4], self.WIDTH, self.HEIGHT)
                                    #   x ratio, y ratio, width ratio, height ratio, image, surface width, surface height, object to return
                                    #   Position ratio, size ratio

    def load_button_images(self, image_paths, scale):
        scaled_images = []

        for path in image_paths:
            # load image
            img = pygame.image.load(path).convert_alpha()
            # scale image
            scaled_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            # Append to list
            scaled_images.append(scaled_img)
        return scaled_images

    def draw_menu(self):
        title_pos = ((self.WIDTH * 0.358), (self.HEIGHT * 0.0926))
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.menu_title, title_pos)

            # Draw buttons and check for button clicks
            start = self.start_button.draw(self.screen)
            data = self.data_button.draw(self.screen)
            analyse = self.analyse_button.draw(self.screen)
            theory = self.theory_button.draw(self.screen)
            exit_menu = self.quit_button.draw(self.screen)

            # Return values when buttons clicked
            if start:
                return 1
            elif data:
                return 2
            elif analyse:
                return 3
            elif theory:
                return 4
            elif exit_menu:
                return 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # Return state machine input
            pygame.display.update()
            self.clock.tick(30)




