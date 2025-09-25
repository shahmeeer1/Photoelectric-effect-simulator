import pygame
import buttons
import sim.DQS as DQS
import Metals
import threading

"""
pygame used for GUI
# buttons. DQS, Metals are my own libraries
Threading used for creating timer for enabling and disabling buttons
lines: 89 - 90


Overriding of __new__ method used from Stackoverflow.
Lines: 39 - 42
https://stackoverflow.com/a/1810367
"""


pygame.init()

# Class for the return button. Subclass of Button. Returns an object or variable when clicked
class ReturnButton(buttons.Button):
    def __init__(self, x_ratio, y_ratio, width_ratio, height_ratio, image, surface_width, surface_height, return_obj):
        super().__init__(x_ratio, y_ratio, width_ratio, height_ratio, image, surface_width, surface_height)
        self.return_obj = return_obj

    def draw(self, surface):
        new_return = super().draw(surface)
        if new_return:
            # return an object of the metal class when clicked
            return True, Metals.Metal(self.return_obj), self.image
        else:
            return False, None, None


class SelectMetals:
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls, screen):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(SelectMetals, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.

    def __init__(self, screen):

        # QueueManager objects to manage selected images and objects using Queues
        self.SelectedImages = DQS.QueueManager(5)
        self.SelectedObjs = DQS.QueueManager(5)

        self.clock = pygame.time.Clock()
        #   Get screen dimensions
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w , info.current_h

        #   Create Game window
        self.screen = screen

        pygame.display.set_caption("Select Metals")

        #   Load and scale background image
        self.background_image = pygame.image.load('Resources/ButtonImages/MenuBackground.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        #   Load and scale menu title image
        self.page_title = pygame.image.load('Resources/Select Metals Images/Title.png').convert_alpha()
        self.page_title = pygame.transform.scale(self.page_title, (self.WIDTH * 0.5156, self.HEIGHT * 0.10532))

        #   Load and scale background rectangle
        self.background_rect = pygame.image.load('Resources/Select Metals Images/BaseRect.png').convert_alpha()
        self.background_rect = pygame.transform.scale(self.background_rect, (self.WIDTH * 0.91146, self.HEIGHT * 0.816))

        #   Load and scale text
        self.selected_text = pygame.image.load('Resources/Select Metals Images/SelectedText.png').convert_alpha()
        self.selected_text = pygame.transform.scale(self.selected_text, (self.WIDTH * 0.12044, self.HEIGHT * 0.03935))

        #   Loaf and scale selection bar
        self.selection_bar = pygame.image.load('Resources/Select Metals Images/SelectionBar.png').convert_alpha()
        self.selection_bar = pygame.transform.scale(self.selection_bar, (self.WIDTH * 0.86458, self.HEIGHT * 0.1169))

        #   Create Buttons
        button_names = [
            "Advance.png", "Quit.png", "Aluminium.png",
            "Beryllium.png", "Caesium.png", "Calcium.png",
            "Cobalt.png", "Gold.png", "Iron.png", "Lead.png",
            "Mercury.png", "Sodium.png", "Uranium.png", "Zinc.png"
        ]
        image_paths = ['Resources/Select Metals Images/SelectButtons/' + i for i in button_names]
        images = self.load_button_images(image_paths, 1)  # Load all images in list

        self.advance_button = buttons.Button(0.7663, 0.8681, 0.1868, 0.09722, images[0], self.WIDTH, self.HEIGHT)

        #   Disable buttons for 1 second1 to avoid miss-clicking
        self.advance_button.DisableAll()
        threading.Timer(0.5, self.advance_button.EnableAll).start()

        self.quit_button = buttons.Button(0.04427, 0.8681, 0.1868, 0.09722, images[1], self.WIDTH, self.HEIGHT)

        # Create metal buttons
        # x position ratio, y position ratio, width ratio, height ratio, image, window dimensions, name of object to return
        self.buttons_list = [

            ReturnButton(0.0807, 0.1875, 0.1868, 0.09722, images[2], self.WIDTH, self.HEIGHT, "Aluminium"),
            ReturnButton(0.2969, 0.1875, 0.1868, 0.09722, images[3], self.WIDTH, self.HEIGHT, "Beryllium"),
            ReturnButton(0.5137, 0.1875, 0.1868, 0.09722, images[4], self.WIDTH, self.HEIGHT, "Caesium"),
            ReturnButton(0.7305, 0.1875, 0.1868, 0.09722, images[5], self.WIDTH, self.HEIGHT, "Calcium"),

            ReturnButton(0.0807, 0.3426, 0.1868, 0.09722, images[6], self.WIDTH, self.HEIGHT, "Cobalt"),
            ReturnButton(0.2969, 0.3426, 0.1868, 0.09722, images[7], self.WIDTH, self.HEIGHT, "Gold"),
            ReturnButton(0.5137, 0.3426, 0.1868, 0.09722, images[8], self.WIDTH, self.HEIGHT, "Iron"),
            ReturnButton(0.7305, 0.3426, 0.1868, 0.09722, images[9], self.WIDTH, self.HEIGHT, "Lead"),

            ReturnButton(0.0807, 0.5069, 0.1868, 0.09722, images[10], self.WIDTH, self.HEIGHT, "Mercury"),
            ReturnButton(0.2969, 0.5069, 0.1868, 0.09722, images[11], self.WIDTH, self.HEIGHT, "Sodium"),
            ReturnButton(0.5137, 0.5069, 0.1868, 0.09722, images[12], self.WIDTH, self.HEIGHT, "Uranium"),
            ReturnButton(0.7305, 0.5069, 0.1868, 0.09722, images[13], self.WIDTH, self.HEIGHT, "Zinc"),
        ]

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

    # Method to draw select metal page gui
    def draw_page(self):
        # positions of static gui elemetns
        title_pos = ((self.WIDTH * 0.2422), (self.HEIGHT * 0.04514))
        selected_text_pos = ((self.WIDTH * 0.07617), (self.HEIGHT * 0.66204))
        background_rect_pos = ((self.WIDTH * 0.04427), (self.HEIGHT * 0.03241))
        selection_bar_pos = ((self.WIDTH * 0.06771), (self.HEIGHT * 0.7095))
        selected_xcoords = [0.08138, 0.25, 0.41862, 0.58724, 0.75586]

        left_button_down = False
        while True:
            self.screen.fill((255, 255, 255))
            pos = pygame.mouse.get_pos()
            #   Draw layout
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.background_rect, background_rect_pos)
            self.screen.blit(self.page_title, title_pos)
            self.screen.blit(self.selected_text, selected_text_pos)
            self.screen.blit(self.selection_bar, selection_bar_pos)

            # advance and quit buttons
            advance = self.advance_button.draw(self.screen)
            quit = self.quit_button.draw(self.screen)
            # button logic
            if advance:
                return 1, self.SelectedObjs.elements()
            elif quit:
                return 2, None


            for i in self.buttons_list:
                # display metal buttons
                clicked, Metal_obj, Metal_image = i.draw(self.screen)
                if clicked: # if button clicked
                    # If the button hasn't already been clicked
                    if Metal_image not in self.SelectedImages.elements():
                        # add its image and returned object to respective queues
                        self.SelectedImages.enqueue(Metal_image)
                        self.SelectedObjs.enqueue(Metal_obj)
                    else:
                        # error message syaing metal ahs already been selected
                        print("Metal Already Selected")

            #   Display selected metals on bar at bottom of screen
            for i in range(5):
                # Iterate through queue elements
                if self.SelectedImages.elements()[i] != "":
                    # Display the image at the bottom of the screen in the correct position based on its position in...
                    # ...the queue
                    scaled_img = pygame.transform.scale(self.SelectedImages.elements()[i],
                                                        (self.WIDTH * 0.1621, self.HEIGHT * 0.09711))
                    self.screen.blit(scaled_img, (self.WIDTH * selected_xcoords[i], self.HEIGHT * 0.71875))
                    img_rect = scaled_img.get_rect(topleft=(self.WIDTH * selected_xcoords[i], self.HEIGHT * 0.71875))
                    self.screen.blit(scaled_img, img_rect.topleft)

                    if img_rect.collidepoint(pos):
                        mouse_state = pygame.mouse.get_pressed()
                        if mouse_state[0] and not left_button_down:
                            # If image at in selected bar clicked
                            left_button_down = True
                            """ Remove the image from the selected images queue so that it will no longer be 
                                displayed in the selected metals bar at the bottom. The positions of the remaining 
                                elements in the queue will be adjusted, and their positions in the selected bar will 
                                be updated accordingly. 
                                
                                Additionally, the corresponding Metal object will be removed from the metal queue, 
                                and the positions of other Metal objects in the queue will be adjusted accordingly.
                            """
                            self.SelectedImages.dequeue(self.SelectedImages.elements()[i])
                            self.SelectedObjs.dequeue(self.SelectedObjs.elements()[i])

            # process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Mouse click logic updated
                    left_button_down = False

            pygame.display.update()
            self.clock.tick(30)

