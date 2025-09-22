import sim.Particles as Particles



class simulator_core:

    def __init__(self, SelectedMetals, dimensions):

        # get list of metals to be used in sim and initialize first ,etal
        self.SelectedMetals = [metal for metal in SelectedMetals if metal != ""]
        self.CurrentMetal = self.SelectedMetals[0]

        self.WIDTH, self.HEIGHT = dimensions

        # Setup particle emitters
        self.Photons = Particles.PhotonEmitter()
        self.Photons.initialise_start_position((0.353, 0.377), (0.3090, 0.38426), self.WIDTH, self.HEIGHT)
        self.Photons.initialise_end_position((0.22656, 0.22786), (0.3819, 0.5058), self.WIDTH, self.HEIGHT)

        self.Electrons = Particles.ElectronEmitter()
        self.Electrons.initialise_start_position((0.23, 0.25), (0.39, 0.5), self.WIDTH, self.HEIGHT)
        self.Electrons.initialise_end_position((0.51,0.51), (0.39, 0.5), self.WIDTH, self.HEIGHT)

        # Set sim limits ofr first metal
        self.initialise_metal()
    
    """ Set sim limits for current metal """
    def initialise_metal(self):
        # Set metal work function value
        self.Electrons.set_WF(self.CurrentMetal.get_Work_Function())
        # Calculate and set max kinetic energy value
        self.max_kinetic_energy = 4.13 - self.Electrons.metal_WF

    """ Switch to next metal in queue """  
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
    
    """ Record the readings for the current metal """
    def Record_readings(self, wavelength, LightIntensity):
        # Append the readings to the results list of the CurrentMetal for insertion into database later on

        self.CurrentMetal.results.append([wavelength, self.Photons.frequency, LightIntensity,
                                         round(self.Electrons.kinetic_energy,2),
                                         self.Electrons.current,
                                         self.Photons.photon_energy])