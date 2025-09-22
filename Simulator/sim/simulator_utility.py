import pygame

class simulator_utility:

    """Method to load button images"""
    @staticmethod
    def load_button_images(image_paths, scale):
        # Method to load button images
        scaled_images = []

        for path in image_paths:
            # load image
            img = pygame.image.load(path).convert_alpha()
            # scale image
            scaled_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            # Append to list
            scaled_images.append(scaled_img)
        return scaled_images

    