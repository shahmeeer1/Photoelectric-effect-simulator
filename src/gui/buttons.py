import pygame

"""
pygame used for gui elements
"""

class Button:
    _Disable = False # clss variable to enable or diable all buttons on screen

    def __init__(self, x_ratio, y_ratio, width_ratio, height_ratio, image, surface_width, surface_height):
        self.top_movement = 0  # Controls animation of button click
        self.x_coord = x_ratio * surface_width
        self.y_coord = y_ratio * surface_height

        # Create button as images
        self.width = int(surface_width * width_ratio)
        self.height = int(surface_height * height_ratio)
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)

        self.clicked = False
        # Base of button
        self.base = pygame.image.load('resources/images/buttons/ButtonBase.png').convert_alpha()
        self.base = pygame.transform.scale(self.base, (self.width, self.height))
        self.FalseTrigger = False
        self.Disable = False

    # Method to disable all buttons on screen by editing class variable
    def DisableAll(self):
        Button._Disable = True

    # Method to enable all buttons on screen by editing class variable
    def EnableAll(self):
        Button._Disable = False


    def draw(self, surface):
        # Draws button on screen
        surface.blit(self.base, (self.x_coord, self.y_coord + 8))  # Button base is slightly below main button
        surface.blit(self.image, (self.x_coord, self.y_coord + self.top_movement))

        pos = pygame.mouse.get_pos()  # Returns mouse position
        if not self.Disable and not Button._Disable:
            #   Logic to prevent accidental mouse triggers
            if pygame.mouse.get_pressed()[0] == 1 and not self.rect.collidepoint(pos):
                self.FalseTrigger = True
            elif self.FalseTrigger and self.rect.collidepoint(pos):
                pass
            else:
                self.FalseTrigger = False
            if not self.FalseTrigger: # If not False click
                if self.rect.collidepoint(pos):  # If mouse hovers over button
                    if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:  # Button now pressed
                        self.clicked = True # set boolean value to true
                        self.top_movement = 8 # Cause button to move down as part of animation in next frame
                        return True

                    elif self.clicked and pygame.mouse.get_pressed()[0] == 0:
                        # when button is not clicked, return variable to false
                        self.clicked = False
                        # Return any recently clicked buttons back to their original positions as part of animation
                        self.top_movement = 0
            # Second reset of button to prevent buttons being frozen in place and prevent reset delays
            if pygame.mouse.get_pressed()[0] == 0:  # If button not currently clicked
                self.clicked = False
                self.top_movement = 0  # This causes the button to move back up
            else:
                pass
            return False




