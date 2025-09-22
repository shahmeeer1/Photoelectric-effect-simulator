import pygame
import pygame_gui
import buttons
import re
import Particles
import random
import threading

"""
pygame and pygame_gui libraries used for gui
re library used for validating user input into simulator
line: 271

random library used for selecting random values
lines: 473, 474, 480, 495, 497, 499
 

# buttons, particles are my own library

threading library used for creating timer for enabling and disabling buttons
lines: 168 - 169

Overriding of __new__ method used from Stackoverflow.
Lines: 41 - 44
https://stackoverflow.com/a/1810367
"""
#test



pygame.init()

# Return button subclass of button class.
class ReturnButton(buttons.Button):
    def __init__(self, x_ratio, y_ratio, width_ratio, height_ratio, image, surface_width, surface_height, return_obj):
        super().__init__(x_ratio, y_ratio, width_ratio, height_ratio, image, surface_width, surface_height)
        self.return_obj = return_obj

    def draw(self, surface):
        new_return = super().draw(surface)
        if new_return:
            return True
        else:
            return False

class Simulation:
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls, SelectedMetals, screen):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(Simulation, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.

    def __init__(self, SelectedMetals, screen):
        #   Get screen dimensions
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h


        #   Create Game window
        self.screen = screen

        self.setup_gui()

        #   Initial sim values
        self.Initial_wavelength = 525.0
        self.Initial_intensity = 50

        #   Particle Emitters
        self.Photons = Particles.PhotonEmitter()
        self.Photons.initialise_start_position((0.353, 0.377), (0.3090, 0.38426), self.WIDTH, self.HEIGHT)
        self.Photons.initialise_end_position((0.22656, 0.22786), (0.3819, 0.5058), self.WIDTH, self.HEIGHT)

        self.Electrons = Particles.ElectronEmitter()
        self.Electrons.initialise_start_position((0.23, 0.25), (0.39, 0.5), self.WIDTH, self.HEIGHT)
        self.Electrons.initialise_end_position((0.51,0.51), (0.39, 0.5), self.WIDTH, self.HEIGHT)

        #   Iterates through the list of selected metals
        self.SelectedMetals = [metal for metal in SelectedMetals if metal != ""]
        self.TotalMetals = len(SelectedMetals)
        self.CurrentMetal = self.SelectedMetals[0]

        # self.Electrons.set_WF(self.CurrentMetal.get_Work_Function)
        self.Electrons.set_WF(self.CurrentMetal.get_Work_Function())

        """     
                max Kinetic Energy = Max Photon Energy - Work Function.
                Since Min Wavelength is 300 nm and 
                Photon Energy = (plank constant * Speed of light)/Max wavelength,
                Max Photon Energy = 4.13    
        """
        self.max_kinetic_energy = 4.13 - self.Electrons.metal_WF



    def error_window(self):
        # Define the dimensions of the error window
        Rect = pygame.Rect(0, 0, self.WIDTH * 0.2, self.HEIGHT * 0.35)
        # Create the error window
        error_window = pygame_gui.elements.UIWindow(Rect, self.manager, "ERROR", "message_window", "#message_window",
                                                    False)
        # Define the error message content
        error_message = pygame_gui.elements.UITextBox("<strong>ARRRR</strong>", Rect, self.manager, False,
                                                      container=error_window)
        # Make the error window blocking, so user cannot interact with buttons below window
        error_window.set_blocking(True)

    def initialise_metal(self):
        # Set metal work function value
        self.Electrons.set_WF(self.CurrentMetal.get_Work_Function())
        # Calculate and set max kinetic energy value
        self.max_kinetic_energy = 4.13 - self.Electrons.metal_WF

    def next_metal(self):
        # Switch to next metal in queue
        # Check if there are more metals in the queue
        if self.SelectedMetals.index(self.CurrentMetal) < len(self.SelectedMetals) - 1:
            # Move to the next metal
            self.CurrentMetal = self.SelectedMetals[self.SelectedMetals.index(self.CurrentMetal) + 1]
            # Initialise the next metal
            self.initialise_metal()
            # Return False to indicate that there are more metals to process
            return False
        # Return true to indicate the simulation is finished
        return True



    def load_button_images(self, image_paths, scale):
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

    def setup_gui(self):
        # Method to setup simulation gui

        pygame.display.set_caption('Simulator')
        #   Load and scale background image
        self.background_image = pygame.image.load('Resources/ButtonImages/MenuBackground.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        #   Load and scale apparatus
        self.apparatus_image = pygame.image.load('Resources/SimulatorImages/Apparatus.png').convert_alpha()
        self.apparatus_image = pygame.transform.scale(self.apparatus_image, (self.WIDTH * 0.5755, self.HEIGHT * 0.7575))

        #   Load and scale light intensity label
        self.light_intensity_label = pygame.image.load('Resources/SimulatorImages/LightIntensityText.png').convert_alpha()
        self.light_intensity_label = pygame.transform.scale(self.light_intensity_label,
                                                            (self.WIDTH * 0.15, self.HEIGHT * 0.04))

        #   Load and scale labels
        self.output_labels = pygame.image.load('Resources/SimulatorImages/OutputLabels.png').convert_alpha()
        self.output_labels = pygame.transform.scale(self.output_labels, (self.WIDTH * 0.1465, self.HEIGHT * 0.4793))

        #   Load and scale colour spectrum
        self.colour_spectrum = pygame.image.load('Resources/SimulatorImages/ColourSpectrum.png').convert_alpha()
        self.colour_spectrum = pygame.transform.scale(self.colour_spectrum, (self.WIDTH * 0.8305, self.HEIGHT * 0.1319))

        #   Create Buttons
        button_names = ["AdvanceButton.png", "QuitButton.png", "RecordButton.png", "ViewButton.png"]
        image_paths = ['Resources/ButtonImages/' + i for i in button_names]
        images = self.load_button_images(image_paths, 1)  # Load all images in list

        self.advance_button = buttons.Button(0.7955, 0.8704, 0.1745, 0.1065, images[0], self.WIDTH, self.HEIGHT)

        #   Disable buttons for 2 seconds to avoid miss-clicking using threading
        #   which will allow the rest of the gui to be setup making the transition smooth
        self.advance_button.DisableAll()
        threading.Timer(1, self.advance_button.EnableAll).start()

        # Create quit, record and view buttons
        self.quit_button = buttons.Button(0.02799, 0.8704, 0.1745, 0.1065, images[1], self.WIDTH, self.HEIGHT)
        self.record_button = buttons.Button(0.4954, 0.8704, 0.13607, 0.1065, images[2], self.WIDTH, self.HEIGHT)
        self.view_button = buttons.Button(0.6452, 0.8704, 0.13607, 0.1065, images[3], self.WIDTH, self.HEIGHT)

        #   Create sliders
        self.manager = pygame_gui.UIManager((int(self.WIDTH), int(self.HEIGHT)), "Resources/Styling/HorizontalSlider.JSON")

        self.spectrum_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((self.WIDTH * 0.037, self.HEIGHT * 0.135), (self.WIDTH * 0.8335, self.HEIGHT * 0.035)),
            525.0,
            (300, 750), manager= self.manager)

        self.light_intensity_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((self.WIDTH * 0.2357, self.HEIGHT * 0.90625), (self.WIDTH * 0.2311, self.HEIGHT * 0.0683)), 50,
            (0, 100), manager= self.manager)

        #   Create Entries
        self.manager.get_theme().load_theme("Resources/Styling/textbox_practise.JSON") # Load widget theme files
        self.manager.get_theme().load_theme("Resources/Styling/temp.JSON")  # pos, size
        self.wavelength_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.WIDTH * 0.8726, self.HEIGHT * 0.01852),
                                      (self.WIDTH * 0.1046, self.HEIGHT * 0.0775)), manager=self.manager,
            object_id="#Wavelength")
        self.wavelength_entry.set_text_length_limit(6) # limit entry length to 6

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

        self.manager.get_theme().load_theme("Resources/Styling/window.JSON")
        self.manager.get_theme().load_theme("Resources/Styling/tempbutton.JSON")


    def return_to_valid_state(self, currentValue):
        try:
            # set wavelength slider to the current value for wavelength
            self.wavelength_entry.set_text(str(currentValue))
            self.spectrum_slider.set_current_value(float(currentValue))

        except:
            # In the case of an error, the frequency slider is reset to its
            # initial state using the initial state attributes
            self.wavelength_entry.set_text(str(self.Initial_wavelength))
            self.spectrum_slider.set_current_value(self.Initial_wavelength)

    def update_spectrum_slider(self, currentValue, inputted_value):
        # The wavelength output box and slider are updated using this method whenever a change takes place.
        try:
            self.spectrum_slider.set_current_value(float(inputted_value))
            self.wavelength_entry.set_text(str(float(inputted_value)))
            self.wavelength_entry.rebuild()
        except:
            # In the case of an error, the error window is displayed and the entry value is reset to the previous value
            self.error_window()
            self.wavelength_entry.set_text(str(currentValue))

    def wavelength_validation(self, currentValue, inputted_value):
        # method to validate wavelength value input using regular expressions
        """
            ([0-9]{,3}): Matches any digits between 0-9 that ois 0-3 digits long
            ([.]([0-9]{1,2}))? : Matches any 1 or 2 digits between 0-9 that are
                                 preceded by a decimal point. The ? signifies that
                                 there must be 0 or 1 of the group preceding it meaning
                                 the input may be integer of float with 1 or 2 digits
                                 after the decimal.
            Examples of valid inputs according to this expression: 123, 1.23, 456.7
        """
        try:
            if re.fullmatch("([0-9]{0,3})([.]([0-9]{1,2}))?", inputted_value):
                if 300.00 <= float(inputted_value) <= 750.00: # only allow inputs between 300 and 750
                    return True
            else:
                return False
        except:
            self.return_to_valid_state(currentValue)
            # resets the input box after invalid input and displays error


    def update_output(self, currentWavelength):
        # Calculate the frequency of the photon using the given current wavelength
        frequency = self.Photons.calc_frequency(currentWavelength)
        # Calculate the energy of the photon
        photon_energy = self.Photons.calc_photon_energy()
        # Calculate the kinetic energy of the electrons using the photon energy
        kinetic_energy = self.Electrons.calc_kinetic_energy(photon_energy)
        # If the kinetic energy is zero, set the current to zero and update the output box accordingly
        if kinetic_energy == 0:
            self.Electrons.current = 0
            self.current_outputbox.set_text("<strong>{} mA</strong>".format(self.Electrons.current))

        # Update the output boxes with the values calculated above
        self.kinetic_energy_outputbox.set_text("<strong>{} eV</strong>".format(round(kinetic_energy,2)))
        self.frequency_outputbox.set_text("<strong>{} THz</strong>".format(round(frequency,2)))
        self.photon_energy_outputbox.set_text("<strong>{} eV</strong>".format(round(photon_energy,2)))

    def update_current(self, currentIntensity):
        # Calculate the threshold energy using the threshold frequency of the current metal and Planck's constant
        threshold_energy = self.CurrentMetal.get_Tfrequency() * self.Photons.plank_constant
        # Calculate the current of the electrons using the threshold energy, photons, and current intensity
        self.Electrons.current = self.Electrons.calc_current(threshold_energy, self.Photons, currentIntensity)
        # Update the current output box with the calculated current value
        self.current_outputbox.set_text("<strong>{} mA</strong>".format(self.Electrons.current))
        # Calculate the proportion of electrons based on the current and update the electrons_proportion attribute
        self.Electrons.electrons_proportion = self.Electrons.min_max(self.Electrons.current, self.Electrons.min_current,
                                                                     self.Electrons.max_current)


    def Emit_Electrons(self, currentIntensity):
        # Check if electrons can be emitted based on the current intensity
        if self.Electrons.check_emit_electron(currentIntensity):
            # If electrons can be emitted, update the current
            self.update_current(currentIntensity)
        else:
            # If electrons cannot be emitted, set kinetic energy and current to zero, and update output boxes
            self.Electrons.kinetic_energy = 0
            self.kinetic_energy_outputbox.set_text("<strong>{} eV</strong>".format(round(self.Electrons.kinetic_energy, 2)))
            self.Electrons.current = 0
            self.current_outputbox.set_text("<strong>{} mA</strong>".format(self.Electrons.current))

    def Record_readings(self, wavelength, LightIntensity):
        # Append the readings to the results list of the CurrentMetal for insertion into database later on

        self.CurrentMetal.results.append([wavelength, self.Photons.frequency, LightIntensity,
                                         round(self.Electrons.kinetic_energy,2),
                                         self.Electrons.current,
                                         self.Photons.photon_energy])


    def View_readings(self):
        # Create a new window to display the results table

        window = pygame_gui.elements.UIWindow(
            pygame.Rect(0.065 * self.WIDTH, 0.12 * self.HEIGHT, self.WIDTH * 0.853, self.HEIGHT * 0.5), self.manager,
            window_display_title="Results Table"
        )

        scrolling_container = pygame_gui.elements.UIScrollingContainer(pygame.Rect((0, 0), window.get_container().get_size()), self.manager, container=window)

        # Headings for the table
        headings = ["Wavelength", "Frequency",
                 "Light\nIntensity", " Kinetic\nEnergy",
                 "Current", " Photon\nEnergy"]

        # Dimensions for the cells and initial position of the table
        cell_width = 0.13 * self.WIDTH
        cell_height = 0.086 * self.HEIGHT
        table_x = 0.032 * self.WIDTH
        table_y = 0.06 * self.HEIGHT

        for index, cell in enumerate(headings):
            # Create text boxes for each heading and add them to the window
            cell_text_box = pygame_gui.elements.UITextBox(
                html_text=cell,
                relative_rect=pygame.Rect((table_x + index * cell_width, table_y),
                                          (cell_width, cell_height)),
                manager=self.manager,
                container=scrolling_container,
                object_id="#Resultsbox"
            )

        # Update table position for data rows
        table_y = 0.145 * self.HEIGHT
        cell_height = 0.0463 * self.HEIGHT

        # Iterate through the 2d array stored at CurrentMetal.results
        for index, row in enumerate(self.CurrentMetal.results):
            # Enumerate returns both the row and the index of the row
            for col_index, cell in enumerate(row):
                # Enumerate returns the data item (cell) and the column number of the item
                cell_text_box = pygame_gui.elements.UITextBox(
                    html_text=str({}).format(cell), # Convert cell data to string and format as HTML
                    relative_rect=pygame.Rect((table_x + col_index * cell_width, table_y + index * cell_height),
                                              (cell_width, cell_height)),
                    manager=self.manager,
                    container=scrolling_container,
                    object_id="#Result"
                )

        height = cell_height * len(self.CurrentMetal.results) + (self.HEIGHT * 0.231)
        length = cell_width * len(headings) + (self.WIDTH * 0.0326)
        # Update dimensions of scrolling container
        scrolling_container.set_scrollable_area_dimensions((length, height))

        # Restrict user interaction with buttons below window
        window.set_blocking(True)
        self.quit_button.DisableAll()

    def reset_sim(self, currentWavelength, currentIntensity):
        # reset the entire simulator by updating all values at the same time
        # This will return the simulators inputs and outputs to the same state they were...
        # ...in at instantiation
        self.intensity_outputbox.set_text("<strong>{}%</strong>".format(currentIntensity))
        self.light_intensity_slider.set_current_value(currentIntensity)
        self.return_to_valid_state(currentWavelength)
        self.update_output(currentWavelength)
        self.update_current(currentIntensity)
        self.Photons.colour = self.Photons.wavelength_to_rgb(currentWavelength)
        self.Electrons.check_emit_electron(currentIntensity)


    def draw_sim(self):
        # Initialise pygame clock for controlling the frame rate
        clock = pygame.time.Clock()

        # Initialise variables for current wavelength and intensity
        currentWavelength = self.Initial_wavelength
        currentIntensity = self.Initial_intensity

        # Define positions for GUI elements on screen
        apparatus_pos = (self.WIDTH * 0.0846, self.HEIGHT * 0.1065)
        spectrum_pos = (self.WIDTH * 0.0384, self.HEIGHT * 0.006944)
        output_labels_pos = (self.WIDTH * 0.8255, self.HEIGHT * 0.2315)
        intensity_label_pos = (self.WIDTH * 0.2357, self.HEIGHT * 0.868)

        # Set initial text for GUI elements
        self.wavelength_entry.set_text(str(currentWavelength))
        self.update_output(currentWavelength)
        self.Emit_Electrons(currentIntensity)

        self.return_to_valid_state(currentWavelength)
        while True:

            # Calculate time since last update
            delta_time = clock.tick(60) / 1000.0

            # Display static GUI elements on screen
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.apparatus_image, apparatus_pos)
            self.screen.blit(self.colour_spectrum, spectrum_pos)
            self.screen.blit(self.output_labels, output_labels_pos)
            self.screen.blit(self.light_intensity_label, intensity_label_pos)



            #   =========== Draw Buttons ===============
            advance = self.advance_button.draw(self.screen)
            quit = self.quit_button.draw(self.screen)
            record = self.record_button.draw(self.screen)
            view = self.view_button.draw(self.screen)

            # ============= Button logic ================
            if record:
                # Save current value of all inputs and outputs
                self.Record_readings(currentWavelength, currentIntensity)
                pass
            if view:
                # View all recorded readings
                self.View_readings()
                pass
            if advance:
                # Advance to next metal in queue or end simulation
                complete = self.next_metal()
                if complete:
                    # No metals left so return to menu
                    return 1
                # Reset wavelength and frequency values to prepare for simulator...
                # ...reset to begin simulating next metal
                currentWavelength = self.Initial_wavelength
                currentIntensity = self.Initial_intensity
                self.reset_sim(currentWavelength, currentIntensity)

            if quit:
                # Return to select metals page
                return 2

            #   =========== Emit Photons ===============

            if random.randint(1,100) < currentIntensity:
                # Photon emission is based on probability.
                # If random value is less than light Intensity value:

                # Create a photon element and add to particles list
                self.Photons.particles.append([self.Photons.colour,
                                               [random.randint(self.Photons.start_x_range[0], self.Photons.start_x_range[1]),
                                                random.randint(self.Photons.start_y_range[0],self.Photons.start_y_range[1])],
                                               [self.WIDTH * 0.59,-(self.HEIGHT * 0.35)]])
                # photon colour, start position, end position, x and y velocity

            # Update positions of photons and draw them on the screen
            for particle in self.Photons.particles:
                # First check if photon position is within allowed range
                if (
                        particle[1][0] < self.Photons.end_x_range[0] and particle[1][1] < self.Photons.end_y_range[0] or
                        particle[1][0] < self.Photons.end_x_range[1] and particle[1][1] < self.Photons.end_y_range[1]
                ):
                    # If not in allowed range, remove photon element from list
                    self.Photons.particles.remove(particle)
                    # Determine if an electron will be emitted or not. Number of electrons cannot exceed number of photons nor can it exceed 120
                    # Number of Electrons also based on probability
                    if self.Electrons.emit_electrons and random.uniform(0,1) < self.Electrons.electrons_proportion and len(self.Electrons.particles) < 120:
                        self.Electrons.particles.append([self.Electrons.colour,
                                                         [random.randint(self.Electrons.start_x_range[0],
                                                                         self.Electrons.start_x_range[1]),
                                                          random.randint(self.Electrons.start_y_range[0],
                                                                         self.Electrons.start_y_range[1])],
                                                         [self.WIDTH * (-((self.Electrons.kinetic_energy - 0) * (600 - 200) / (self.max_kinetic_energy - 0) + 200) )/1536, 0]])
                                                        # Electron velocity = (ke - min_ke) * (max_speed_electron - min_speed_electron) / (max_ke - min_ke) + min_speed_electron
                        # Electron colour, start position, end position, x and y velocity
                    continue

                # Update position of photon, making them move across screen
                particle[1][0] -= particle[2][0] * delta_time
                particle[1][1] -= particle[2][1] * delta_time
                # Draw photon
                pygame.draw.circle(self.screen,
                                   particle[0],
                                   particle[1],
                                   self.Photons.radius)

            #   ===========Emit Electrons ===============

            # Check if the electron is still within range
            for particle in self.Electrons.particles:
                if(
                        particle[1][0] > self.Electrons.end_x_range[0]
                ):
                    # If it is outside the allowed range, remove the electron
                    self.Electrons.particles.remove(particle)
                    continue
                # Update the position of the electron by adding its velocity as a multiple of delta_time
                particle[1][0] -= particle[2][0] * delta_time
                pygame.draw.circle(self.screen,
                                   particle[0],
                                   particle[1],
                                   self.Electrons.radius)

                #===========================================

            # ========== Event Loop ==========

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                #   User updates wavelength by moving slider
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.spectrum_slider:
                        #   check that slider has moved and not just been held down
                        if round(event.value,2) != currentWavelength:
                            #   round the new slider value to 2 dp.
                            currentWavelength = round(event.value, 2)
                            #   update the value of the wavelength entry
                            self.wavelength_entry.set_text(str(currentWavelength))
                            # Update photons colour
                            self.Photons.colour = self.Photons.wavelength_to_rgb(currentWavelength)
                            # Calculate new values of other outputs (frequency, kinetic energy etc.)
                            self.update_output(currentWavelength)
                            # Check if electrons can be emitted
                            self.Emit_Electrons(currentIntensity)

                    elif event.ui_element == self.light_intensity_slider:
                        #   check that value has changed
                        if event.value != currentIntensity:
                            currentIntensity = event.value
                            #   update intensity outputbox
                            self.intensity_outputbox.set_text("<strong>{}%</strong>".format(currentIntensity))
                            # Update other output values (frequency, kinetic energy etc.)
                            self.update_output(currentWavelength)
                            # Check if electrons can be emitted
                            self.Emit_Electrons(currentIntensity)

                #   User inputs wavelength value
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#Wavelength":
                    #   retrieve inputted value from wavelength entry box
                    inputted_value = self.wavelength_entry.get_text()
                    #   check if the value is valid
                    if self.wavelength_validation(currentWavelength, inputted_value):
                        #   update the slider to the new wavelength value
                        self.update_spectrum_slider(currentWavelength, inputted_value)
                        #   update the new currentValue
                        currentWavelength = float(inputted_value)
                        # Update photons colour
                        self.Photons.colour = self.Photons.wavelength_to_rgb(currentWavelength)
                        # Calculate new values of other outputs (frequency, kinetic energy etc.)
                        self.update_output(currentWavelength)
                        # Check if electrons can be emitted
                        self.Emit_Electrons(currentIntensity)
                    else:
                        #   return wavelength entry to initial value before invalid input
                        self.wavelength_entry.set_text(str(currentWavelength))
                        # Reset wavelength entry box after inputting value
                        self.wavelength_entry.rebuild()
                        self.wavelength_entry.unfocus()
                        #   display error
                        print("Invalid input")
                        self.error_window()
                elif event.type == pygame_gui.UI_WINDOW_CLOSE:
                    self.quit_button.EnableAll()

        # Update pygame and pygame_gui managers and window
                self.manager.process_events(event)

            self.manager.update(delta_time)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

