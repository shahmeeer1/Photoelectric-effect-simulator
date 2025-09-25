import pygame
import pygame_gui
import gui.buttons as buttons

"""
pygame and pygame_gui used for GUI

# buttons is my own library


Overriding of __new__ method used from Stackoverflow.
Lines: 22 - 24
https://stackoverflow.com/a/1810367

Image: 'Image1.png" from wikipedia
https://commons.wikimedia.org/wiki/File:Photoelectric_effect.svg
"""

pygame.init()

class Theory:
    _instance = None

    def __new__(cls, screen):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(Theory, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.


    def __init__(self, screen):
        # Retrieve screen data
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        self.screen = screen
        pygame.display.set_caption('Theory')

        # Load simulator images
        self.background_image = pygame.image.load('resources/images/view_data/MenuBackground.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        self.bgrect_image = pygame.image.load('resources/images/theory_images/backgroundrect.png').convert_alpha()
        self.bgrect_image = pygame.transform.scale(self.bgrect_image, self.scaleT((1477, 760)))

        self.Title_image = pygame.image.load('resources/images/theory_images/TheoryTitle.png').convert_alpha()
        self.Title_image = pygame.transform.scale(self.Title_image, self.scaleT((241, 82)))

        self.page1_image = pygame.image.load('resources/images/theory_images/page1.png').convert_alpha()
        self.page1_image = pygame.transform.scale(self.page1_image, self.scaleT((1420, 719)))

        self.page2_image = pygame.image.load('resources/images/theory_images/page2.png').convert_alpha()
        self.page2_image = pygame.transform.scale(self.page2_image, self.scaleT((1420, 637)))

        self.image1 = pygame.image.load('resources/images/theory_images/PEimg1.png').convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, self.scaleT((273, 184)))

        # Create simulator buttons
        self.QuitButton_image = pygame.image.load('resources/images/buttons/QuitButton.png').convert_alpha()
        self.QuitButton = buttons.Button(0.82, 0.84, 0.1758, 0.1146, self.QuitButton_image, self.WIDTH, self.HEIGHT)

        self.ui_manager = pygame_gui.UIManager((int(self.WIDTH), int(self.HEIGHT)), "resources/styles/ButtonTheme.JSON")
        self.page1_button = pygame_gui.elements.UIButton(pygame.Rect(self.scaleT((1319, 542)), self.scaleT((118, 50))), "Page 1", manager= self.ui_manager, object_id= "#ViewData")
        self.page2_button = pygame_gui.elements.UIButton(pygame.Rect(self.scaleT((1319, 617)), self.scaleT((118, 50))), "Page 2", manager= self.ui_manager, object_id= "#ViewData")

    # Method to scale dimensions to appropriate window size
    def scaleT(self, tuple):
        return (((self.WIDTH * tuple[0]) / 1536), ((self.HEIGHT * tuple[1]) / 864))

    # Method to run gameloop
    def draw_page(self):
        clock = pygame.time.Clock()

        # Positions of GUI elements
        bgrect_pos = self.scaleT((29, 78))
        title_pos = self.scaleT((647, 15))
        page1_pos = self.scaleT((86, 97))
        page2_pos = self.scaleT((58, 115))
        image1_pos = self.scaleT((1092, 155))
        page = 1
        self.page1_button.disable()

        while True:
            # Initialise click
            time_delta = clock.tick(60) / 1000.0

            # Blit images onto screen
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.bgrect_image, bgrect_pos)
            self.screen.blit(self.Title_image, title_pos)
            self.screen.blit(self.image1, image1_pos)

            quit = self.QuitButton.draw(self.screen)

            # quit button logic
            if quit:
                return 1

            # page 1 and 2 buttons logic
            if page == 1:
                # If we are currently on page 1 blit the page 1 text
                self.screen.blit(self.page1_image, page1_pos)
            elif page == 2:
                # If we are on page 2, blit the page 2 text
                self.screen.blit(self.page2_image, page2_pos)

            for event in pygame.event.get():
                # quit pygame if window closed
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Page 1 and 2 button logic
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.page1_button.check_pressed():
                        # If page 1 button clicked
                        self.page1_button.disable()
                        # Disable the button
                        self.page2_button.enable()
                        # Enable the page 2 button
                        page = 1
                        # Set the current page to 1
                    elif self.page2_button.check_pressed():
                        # If page 2 button clicked
                        self.page2_button.disable()
                        # Disable the button
                        self.page1_button.enable()
                        # Enable the page 1 button
                        page = 2
                        # Set the current page to 1


        # Update pygame and pygame_ui managers and screen

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()
