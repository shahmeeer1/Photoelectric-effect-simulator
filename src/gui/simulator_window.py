import pygame
import pygame_gui
import gui.buttons as buttons


from core.simulator_core import simulator_core as SimCore
from gui.gui_manager import GUIManager
from gui.gui_validation import GUIValidation
from gui.simulation_draw import SimulationDraw



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

        pygame.display.set_caption('Simulator')

        #   Initial sim values  # POSSIBLE EXTRACTION   
        self.Initial_wavelength = 525.0
        self.Initial_intensity = 50

        self.SimCore = SimCore(SelectedMetals, (self.WIDTH, self.HEIGHT))  # Initialise simulator core
        self.gui = GUIManager((self.WIDTH, self.HEIGHT), self.screen)
        self.validation = GUIValidation(self.gui, self.Initial_wavelength)
        self.simDraw = SimulationDraw(self.gui, self.SimCore, (self.WIDTH, self.HEIGHT), self.screen)


    """Gui related"""
    def error_window(self):
        # Define the dimensions of the error window
        Rect = pygame.Rect(0, 0, self.WIDTH * 0.2, self.HEIGHT * 0.35)
        # Create the error window
        error_window = pygame_gui.elements.UIWindow(Rect, self.gui.manager, "ERROR", "message_window", "#message_window",
                                                    False)
        # Define the error message content
        error_message = pygame_gui.elements.UITextBox("<strong>ARRRR</strong>", Rect, self.gui.manager, False,
                                                      container=error_window)
        # Make the error window blocking, so user cannot interact with buttons below window
        error_window.set_blocking(True)



    """Both"""  #   POSSIBLE EXTRACTION
    def update_output(self, currentWavelength):
        freq, pe, ke, crnt = self.SimCore.update_output(currentWavelength)

        if ke == 0:
            self.gui.current_outputbox.set_text("<strong>{} mA</strong>".format(crnt))

        # Update the output boxes with the values calculated above
        self.gui.kinetic_energy_outputbox.set_text("<strong>{} eV</strong>".format(round(ke,2)))
        self.gui.frequency_outputbox.set_text("<strong>{} THz</strong>".format(round(freq,2)))
        self.gui.photon_energy_outputbox.set_text("<strong>{} eV</strong>".format(round(pe,2)))

    """Both"""  #   POSSIBLE EXTRACTION
    def update_current(self, currentIntensity):
        # Calculate the threshold energy using the threshold frequency of the current metal and Planck's constant
        threshold_energy = self.SimCore.CurrentMetal.get_Tfrequency() * self.SimCore.Photons.plank_constant
        # Calculate the current of the electrons using the threshold energy, photons, and current intensity
        self.SimCore.Electrons.current = self.SimCore.Electrons.calc_current(threshold_energy, self.SimCore.Photons, currentIntensity)
        # Update the current output box with the calculated current value
        self.gui.current_outputbox.set_text("<strong>{} mA</strong>".format(self.SimCore.Electrons.current))
        # Calculate the proportion of electrons based on the current and update the electrons_proportion attribute
        self.SimCore.Electrons.electrons_proportion = self.SimCore.Electrons.min_max(self.SimCore.Electrons.current, self.SimCore.Electrons.min_current,
                                                                     self.SimCore.Electrons.max_current)

    """Gui related"""
    def Emit_Electrons(self, currentIntensity):
        # Check if electrons can be emitted based on the current intensity
        if self.SimCore.Electrons.check_emit_electron(currentIntensity):
            # If electrons can be emitted, update the current
            self.update_current(currentIntensity)
        else:
            # If electrons cannot be emitted, set kinetic energy and current to zero, and update output boxes
            self.SimCore.Electrons.kinetic_energy = 0
            self.gui.kinetic_energy_outputbox.set_text("<strong>{} eV</strong>".format(round(self.SimCore.Electrons.kinetic_energy, 2)))
            self.SimCore.Electrons.current = 0
            self.gui.current_outputbox.set_text("<strong>{} mA</strong>".format(self.SimCore.Electrons.current))

    """Gui related"""
    def View_readings(self):
        # Create a new window to display the results table

        window = pygame_gui.elements.UIWindow(
            pygame.Rect(0.065 * self.WIDTH, 0.12 * self.HEIGHT, self.WIDTH * 0.853, self.HEIGHT * 0.5), self.gui.manager,
            window_display_title="Results Table"
        )

        scrolling_container = pygame_gui.elements.UIScrollingContainer(pygame.Rect((0, 0), window.get_container().get_size()), self.gui.manager, container=window)

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
                manager=self.gui.manager,
                container=scrolling_container,
                object_id="#Resultsbox"
            )

        # Update table position for data rows
        table_y = 0.145 * self.HEIGHT
        cell_height = 0.0463 * self.HEIGHT

        # Iterate through the 2d array stored at CurrentMetal.results
        for index, row in enumerate(self.SimCore.CurrentMetal.results):
            # Enumerate returns both the row and the index of the row
            for col_index, cell in enumerate(row):
                # Enumerate returns the data item (cell) and the column number of the item
                cell_text_box = pygame_gui.elements.UITextBox(
                    html_text=str({}).format(cell), # Convert cell data to string and format as HTML
                    relative_rect=pygame.Rect((table_x + col_index * cell_width, table_y + index * cell_height),
                                              (cell_width, cell_height)),
                    manager=self.gui.manager,
                    container=scrolling_container,
                    object_id="#Result"
                )

        height = cell_height * len(self.SimCore.CurrentMetal.results) + (self.HEIGHT * 0.231)
        length = cell_width * len(headings) + (self.WIDTH * 0.0326)
        # Update dimensions of scrolling container
        scrolling_container.set_scrollable_area_dimensions((length, height))

        # Restrict user interaction with buttons below window
        window.set_blocking(True)
        self.gui.quit_button.DisableAll()

    """Both"""  #  POSSIBLE EXTRACTION
    def reset_sim(self, currentWavelength, currentIntensity):
        # reset the entire simulator by updating all values at the same time
        # This will return the simulators inputs and outputs to the same state they were...
        # ...in at instantiation
        self.gui.intensity_outputbox.set_text("<strong>{}%</strong>".format(currentIntensity))
        self.gui.light_intensity_slider.set_current_value(currentIntensity)
        self.validation.return_to_valid_state(currentWavelength)
        self.update_output(currentWavelength)
        self.update_current(currentIntensity)
        self.SimCore.Photons.colour = self.SimCore.Photons.wavelength_to_rgb(currentWavelength)
        self.SimCore.Electrons.check_emit_electron(currentIntensity)

    """Both"""
    def draw_sim(self):
        # Initialise pygame clock for controlling the frame rate
        clock = pygame.time.Clock()

        # Initialise variables for current wavelength and intensity
        currentWavelength = self.Initial_wavelength
        currentIntensity = self.Initial_intensity


        # Set initial text for GUI elements
        self.gui.wavelength_entry.set_text(str(currentWavelength))
        self.update_output(currentWavelength)
        self.Emit_Electrons(currentIntensity)

        self.validation.return_to_valid_state(currentWavelength)
        while True:

            # Calculate time since last update
            delta_time = clock.tick(60) / 1000.0

            # draw statiic elements of screen
            self.simDraw.draw_static()

            #   =========== Draw Buttons ===============
            advance = self.gui.advance_button.draw(self.screen)
            quit = self.gui.quit_button.draw(self.screen)
            record = self.gui.record_button.draw(self.screen)
            view = self.gui.view_button.draw(self.screen)

            # ============= Button logic ================
            if record:
                # Save current value of all inputs and outputs
                self.SimCore.Record_readings(currentWavelength, currentIntensity)
                pass
            if view:
                # View all recorded readings
                self.View_readings()
                pass
            if advance:
                # Advance to next metal in queue or end simulation
                complete = self.SimCore.next_metal()
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

            #   =========== Emit Particles ===============

            self.simDraw.emit_particles(currentIntensity, delta_time)

            # ========== Event Loop ==========

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                #   User updates wavelength by moving slider
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.gui.spectrum_slider:
                        #   check that slider has moved and not just been held down
                        if round(event.value,2) != currentWavelength:
                            #   round the new slider value to 2 dp.
                            currentWavelength = round(event.value, 2)
                            #   update the value of the wavelength entry
                            self.gui.wavelength_entry.set_text(str(currentWavelength))
                            # Update photons colour
                            self.SimCore.Photons.colour = self.SimCore.Photons.wavelength_to_rgb(currentWavelength)
                            # Calculate new values of other outputs (frequency, kinetic energy etc.)
                            self.update_output(currentWavelength)
                            # Check if electrons can be emitted
                            self.Emit_Electrons(currentIntensity)

                    elif event.ui_element == self.gui.light_intensity_slider:
                        #   check that value has changed
                        if event.value != currentIntensity:
                            currentIntensity = event.value
                            #   update intensity outputbox
                            self.gui.intensity_outputbox.set_text("<strong>{}%</strong>".format(currentIntensity))
                            # Update other output values (frequency, kinetic energy etc.)
                            self.update_output(currentWavelength)
                            # Check if electrons can be emitted
                            self.Emit_Electrons(currentIntensity)

                #   User inputs wavelength value
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#Wavelength":
                    #   retrieve inputted value from wavelength entry box
                    inputted_value = self.gui.wavelength_entry.get_text()
                    #   check if the value is valid
                    if self.validation.wavelength_validation(currentWavelength, inputted_value):
                        #   update the slider to the new wavelength value
                        self.validation.update_spectrum_slider(currentWavelength, inputted_value)
                        #   update the new currentValue
                        currentWavelength = float(inputted_value)
                        # Update photons colour
                        self.SimCore.Photons.colour = self.SimCore.Photons.wavelength_to_rgb(currentWavelength)
                        # Calculate new values of other outputs (frequency, kinetic energy etc.)
                        self.update_output(currentWavelength)
                        # Check if electrons can be emitted
                        self.Emit_Electrons(currentIntensity)
                    else:
                        #   return wavelength entry to initial value before invalid input
                        self.gui.wavelength_entry.set_text(str(currentWavelength))
                        # Reset wavelength entry box after inputting value
                        self.gui.wavelength_entry.rebuild()
                        self.gui.wavelength_entry.unfocus()
                        #   display error
                        print("Invalid input")
                        self.error_window()
                elif event.type == pygame_gui.UI_WINDOW_CLOSE:
                    self.gui.quit_button.EnableAll()

        # Update pygame and pygame_gui managers and window
                self.gui.manager.process_events(event)

            self.gui.manager.update(delta_time)
            self.gui.manager.draw_ui(self.screen)
            pygame.display.update()

