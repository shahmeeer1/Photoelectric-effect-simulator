import random
from sim.simulator_core import simulator_core as SimCore
import pygame

class SimulationDraw:
    
    def __init__(self, guimanager, simcore, dimensions, screen):
        self.gui = guimanager
        self.SimCore = simcore
        self.WIDTH, self.HEIGHT = dimensions
        self.screen = screen

        self._static_positions()

    
    def _static_positions(self):
        # Define positions for GUI elements on screen
        self.apparatus_pos = (self.WIDTH * 0.0846, self.HEIGHT * 0.1065)
        self.spectrum_pos = (self.WIDTH * 0.0384, self.HEIGHT * 0.006944)
        self.output_labels_pos = (self.WIDTH * 0.8255, self.HEIGHT * 0.2315)
        self.intensity_label_pos = (self.WIDTH * 0.2357, self.HEIGHT * 0.868)


    def draw_static(self):

        # Display static GUI elements on screen
        self.screen.blit(self.gui.background_image, (0, 0))
        self.screen.blit(self.gui.apparatus_image, self.apparatus_pos)
        self.screen.blit(self.gui.colour_spectrum, self.spectrum_pos)
        self.screen.blit(self.gui.output_labels, self.output_labels_pos)
        self.screen.blit(self.gui.light_intensity_label, self.intensity_label_pos)

    def emit_particles(self, currentIntensity, delta_time):

        self._emit_photons(currentIntensity, delta_time)
        self._emit_electrons(delta_time)

    
    def _emit_photons(self,currentIntensity, delta_time):
         
        if random.randint(1,100) < currentIntensity:
            # Photon emission is based on probability.
            # If random value is less than light Intensity value:

            # Create a photon element and add to particles list
            self.SimCore.Photons.particles.append([self.SimCore.Photons.colour,
                                            [random.randint(self.SimCore.Photons.start_x_range[0], self.SimCore.Photons.start_x_range[1]),
                                            random.randint(self.SimCore.Photons.start_y_range[0],self.SimCore.Photons.start_y_range[1])],
                                            [self.WIDTH * 0.59,-(self.HEIGHT * 0.35)]])
            # photon colour, start position, end position, x and y velocity

        # Update positions of photons and draw them on the screen
        for particle in self.SimCore.Photons.particles:
            # First check if photon position is within allowed range
            if (
                    particle[1][0] < self.SimCore.Photons.end_x_range[0] and particle[1][1] < self.SimCore.Photons.end_y_range[0] or
                    particle[1][0] < self.SimCore.Photons.end_x_range[1] and particle[1][1] < self.SimCore.Photons.end_y_range[1]
            ):
                # If not in allowed range, remove photon element from list
                self.SimCore.Photons.particles.remove(particle)
                # Determine if an electron will be emitted or not. Number of electrons cannot exceed number of photons nor can it exceed 120
                # Number of Electrons also based on probability
                if self.SimCore.Electrons.emit_electrons and random.uniform(0,1) < self.SimCore.Electrons.electrons_proportion and len(self.SimCore.Electrons.particles) < 120:
                    self.SimCore.Electrons.particles.append([self.SimCore.Electrons.colour,
                                                        [random.randint(self.SimCore.Electrons.start_x_range[0],
                                                                        self.SimCore.Electrons.start_x_range[1]),
                                                        random.randint(self.SimCore.Electrons.start_y_range[0],
                                                                        self.SimCore.Electrons.start_y_range[1])],
                                                        [self.WIDTH * (-((self.SimCore.Electrons.kinetic_energy - 0) * (600 - 200) / (self.SimCore.max_kinetic_energy - 0) + 200) )/1536, 0]])
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
                                self.SimCore.Photons.radius)

    
    def _emit_electrons(self, delta_time):
            
        # Check if the electron is still within range
            for particle in self.SimCore.Electrons.particles:
                if(
                        particle[1][0] > self.SimCore.Electrons.end_x_range[0]
                ):
                    # If it is outside the allowed range, remove the electron
                    self.SimCore.Electrons.particles.remove(particle)
                    continue
                # Update the position of the electron by adding its velocity as a multiple of delta_time
                particle[1][0] -= particle[2][0] * delta_time
                pygame.draw.circle(self.screen,
                                   particle[0],
                                   particle[1],
                                   self.SimCore.Electrons.radius)
    

