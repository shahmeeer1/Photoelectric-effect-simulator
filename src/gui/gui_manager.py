import pygame
import pygame_gui
import gui.buttons as buttons
from utils.simulator_utility import simulator_utility
import threading

class GUIManager:
    def __init__(self, dimensions, screen):

        self.WIDTH, self.HEIGHT = dimensions
        self.screen = screen

        
        self.manager = pygame_gui.UIManager(dimensions)


        self._load_images()
        self._setup_buttons()
        self._setup_sliders()
        self._setup_text_entries()
        self._setup_text_boxes()
    

    def _load_images(self):

        #   Load and scale background image
        self.background_image = pygame.image.load('resources/images/buttons/MenuBackground.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        #   Load and scale apparatus
        self.apparatus_image = pygame.image.load('resources/images/simulator_images/Apparatus.png').convert_alpha()
        self.apparatus_image = pygame.transform.scale(self.apparatus_image, (self.WIDTH * 0.5755, self.HEIGHT * 0.7575))

        #   Load and scale light intensity label
        self.light_intensity_label = pygame.image.load('resources/images/simulator_images/LightIntensityText.png').convert_alpha()
        self.light_intensity_label = pygame.transform.scale(self.light_intensity_label,
                                                            (self.WIDTH * 0.15, self.HEIGHT * 0.04))

        #   Load and scale labels
        self.output_labels = pygame.image.load('resources/images/simulator_images/OutputLabels.png').convert_alpha()
        self.output_labels = pygame.transform.scale(self.output_labels, (self.WIDTH * 0.1465, self.HEIGHT * 0.4793))

        #   Load and scale colour spectrum
        self.colour_spectrum = pygame.image.load('resources/images/simulator_images/ColourSpectrum.png').convert_alpha()
        self.colour_spectrum = pygame.transform.scale(self.colour_spectrum, (self.WIDTH * 0.8305, self.HEIGHT * 0.1319))

    def _setup_buttons(self):

        #   Create Buttons
        button_names = ["AdvanceButton.png", "QuitButton.png", "RecordButton.png", "ViewButton.png"]
        image_paths = ['resources/images/buttons/' + i for i in button_names]
        images = simulator_utility.load_button_images(image_paths, 1)  # Load all images in list

        self.advance_button = buttons.Button(0.7955, 0.8704, 0.1745, 0.1065, images[0], self.WIDTH, self.HEIGHT)

        #   Disable buttons for 2 seconds to avoid miss-clicking using threading
        #   which will allow the rest of the gui to be setup making the transition smooth
        self.advance_button.DisableAll()
        threading.Timer(1, self.advance_button.EnableAll).start()

        # Create quit, record and view buttons
        self.quit_button = buttons.Button(0.02799, 0.8704, 0.1745, 0.1065, images[1], self.WIDTH, self.HEIGHT)
        self.record_button = buttons.Button(0.4954, 0.8704, 0.13607, 0.1065, images[2], self.WIDTH, self.HEIGHT)
        self.view_button = buttons.Button(0.6452, 0.8704, 0.13607, 0.1065, images[3], self.WIDTH, self.HEIGHT)

    def _setup_sliders(self):
        
        self.manager = pygame_gui.UIManager((int(self.WIDTH), int(self.HEIGHT)), "resources/styles/HorizontalSlider.JSON")

        self.spectrum_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((self.WIDTH * 0.037, self.HEIGHT * 0.135), (self.WIDTH * 0.8335, self.HEIGHT * 0.035)),
            525.0,
            (300, 750), manager= self.manager)

        self.light_intensity_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((self.WIDTH * 0.2357, self.HEIGHT * 0.90625), (self.WIDTH * 0.2311, self.HEIGHT * 0.0683)), 50,
            (0, 100), manager= self.manager)
    
    def _setup_text_entries(self):
        #   Create Entries
        self.manager.get_theme().load_theme("resources/styles/textbox_practise.JSON") # Load widget theme files
        self.manager.get_theme().load_theme("resources/styles/temp.JSON")  # pos, size
        self.wavelength_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.WIDTH * 0.8726, self.HEIGHT * 0.01852),
                                      (self.WIDTH * 0.1046, self.HEIGHT * 0.0775)), manager=self.manager,
            object_id="#Wavelength")
        self.wavelength_entry.set_text_length_limit(6) # limit entry length to 6
    
    def _setup_text_boxes(self):
        #   create textboxes
        # These textboxes output the current value for their respective attributes
        # Made using pygame_ui library

        self.frequency_outputbox = pygame_gui.elements.UITextBox("<strong> THz</strong>",
                                                                 pygame.Rect(self.WIDTH * 0.8255, self.HEIGHT * 0.2731,
                                                                             self.WIDTH * 0.13, self.HEIGHT * 0.07755),
                                                                 self.manager, False, object_id="#Frequency")

        self.photon_energy_outputbox = pygame_gui.elements.UITextBox("<strong> eV</strong>",
                                                                     pygame.Rect(self.WIDTH * 0.8255,
                                                                                 self.HEIGHT * 0.42477,
                                                                                 self.WIDTH * 0.13,
                                                                                 self.HEIGHT * 0.07755), self.manager,
                                                                     False, object_id="#PhotonEnergy")

        self.kinetic_energy_outputbox = pygame_gui.elements.UITextBox("<strong> eV</strong>",
                                                                      pygame.Rect(self.WIDTH * 0.8255,
                                                                                  self.HEIGHT * 0.57639,
                                                                                  self.WIDTH * 0.13,
                                                                                  self.HEIGHT * 0.07755), self.manager,
                                                                      False, object_id="#KineticEnergy")

        self.current_outputbox = pygame_gui.elements.UITextBox("<strong> mA</strong>",
                                                               pygame.Rect(self.WIDTH * 0.8255, self.HEIGHT * 0.72801,
                                                                           self.WIDTH * 0.13, self.HEIGHT * 0.07755),
                                                               self.manager, False, object_id="#Current")

        self.intensity_outputbox = pygame_gui.elements.UITextBox("<strong>50%</strong>",
                                                                 pygame.Rect(self.WIDTH * 0.39, self.HEIGHT * 0.868,
                                                                             self.WIDTH * 0.071, self.HEIGHT * 0.045),
                                                                 self.manager, False, object_id="#Intensity")

        self.manager.get_theme().load_theme("resources/styles/window.JSON")
        self.manager.get_theme().load_theme("resources/styles/tempbutton.JSON")