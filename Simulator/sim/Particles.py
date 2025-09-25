# Parent class for particle emitters
class ParticleEmitter:

    def __init__(self):
        # Initialize properties common to all particle emitters

        self.particles = []
        self.radius = 6
        # Range for where particles can be created
        self.start_x_range = ()
        self.start_y_range = ()
        # Range for where particles will be deleted
        self.end_x_range = ()
        self.end_y_range = ()
        # Default colour of particles
        self.colour = (0,255,0)
        self.plank_constant = 6.62606e-34 # Planck constant in joule-seconds
        self.speed_of_light = 3e8 # Speed of light in meters per second

    def initialise_start_position(self, x_ratio, y_ratio, screen_width, screen_height):
        # Initialize start position ranges based on ratios and screen dimensions
        self.start_x_range = (int((x_ratio[0] * screen_width)),int((x_ratio[1] * screen_width)))
        self.start_y_range = (int((y_ratio[0] * screen_height)),int((y_ratio[1] * screen_height)))

    def initialise_end_position(self, x_ratio, y_ratio, screen_width, screen_height):
        # Initialize end position ranges based on ratios and screen dimensions
        self.end_x_range = (int((x_ratio[0] * screen_width)),int((x_ratio[1] * screen_width)))
        self.end_y_range = (int((y_ratio[0] * screen_height)),int((y_ratio[1] * screen_height)))

    def joules_to_ev(self, joules):
        # Convert joules to electron-volts
        joules_to_eV_factor = 6.242e18  # 1 joule = 6.242e18 electron-volts
        eV = joules * joules_to_eV_factor
        return eV

    def ev_to_joules(self, eV):
        # Convert electron-volts to joules
        eV_to_joules_factor = 1.602e-19  # 1 eV = 1.602e-19 joules
        joules = eV * eV_to_joules_factor
        return joules

    def hertz_to_terahertz(self, hertz):
        # Convert hertz to terahertz
        terahertz = hertz / 1e12
        return terahertz

    def terahertz_to_hertz(self, terahertz):
        # Convert terahertz to hertz
        hertz = terahertz * 1e12
        return hertz

    def metres_to_nan0metres(self, metres):
        # Convert meters to nanometers
        nanometres = metres * 1e-9
        return nanometres



# Class for photon particle emitter
class PhotonEmitter(ParticleEmitter):
    def __init__(self):
        super().__init__()
        self.frequency = 571.4 # Default frequency stored in terahertz
        self.photon_energy = 2.365 # Default photon energy stored in electron-volts
        self.lamp_power = 10 # Default lamp power stored in watts

    def wavelength_to_rgb(self,wavelength):
        # Convert wavelength to RGB colour
        r = 0
        g = 0
        b = 0
        if 300 <= wavelength < 303:
            r = 0
            g = 0
            b = 0
        elif 303 <= wavelength < 315:
            r = 127
            g = 0
            b = 255
        elif 315 <= wavelength < 330:
            #   Indigo
            r = 75
            g = 0
            b = 130

        elif 330 <= wavelength < 415:
            # blue
            r = 0
            g = 0
            b = 255
        elif 415 <= wavelength < 560:
            # green
            r = 0
            g = 255
            b = 0
        elif 560 <= wavelength < 590:
            # yellow
            r = 255
            g = 255
            b = 0.0
        elif 590 <= wavelength < 630:
            # orange
            r = 255
            g = 130
            b = 0.0
        elif 630 <= wavelength <= 710:
            #   red
            r = 255
            g = 0
            b = 0
        else:
            r = 0
            g = 0
            b = 0
        return (r, g, b)



    def calc_frequency(self,wavelength):
        # Calculate frequency based on wavelength
        self.frequency = round(self.hertz_to_terahertz((self.speed_of_light / (wavelength * 1e-9))),2)
        return self.frequency

    def calc_photon_energy(self):
        # Calculate photon energy based on frequency
        self.photon_energy = round(self.joules_to_ev(self.plank_constant * self.terahertz_to_hertz(self.frequency)),2)
        return self.photon_energy

    def no_of_photons(self, intensity):
        # Calculate number of photons based on lamp power and intensity
        N = self.lamp_power / self.ev_to_joules(self.photon_energy)
        return N * (intensity/100)




class ElectronEmitter(ParticleEmitter):
    def __init__(self):
        super().__init__()
        self.kinetic_energy = 0 # Default kinetic energy stored in electronvolts
        self.metal_WF= 0 # Work function of the metal stored in electronvolts
        self.elementary_charge = 1.60e-19 # Elementary charge in coulombs
        self.current = 0 # Default current stored in picoamperes
        self.emit_electrons = False # Flag to indicate electron emission
        self.electrons_proportion = 1 # Proportion of emitted electrons
        self.max_current = 999 # Maximum theoretical current in picoamperes
        self.min_current = 0 # Minimum theoretical current in picoamperes
        self.radius = 4 # Default radius of emitted electrons
        self.colour = (125, 249, 255) # Default colour for emitted electrons

    def calc_kinetic_energy(self, photon_energy):
        # Calculate kinetic energy of emitted electrons
        if photon_energy > self.metal_WF:
            # if photon energy less than work energy of metal
            self.kinetic_energy = photon_energy - self.metal_WF
            if self.kinetic_energy > 0:
                return self.kinetic_energy
        # If photon energy is less than work function, kinetic energy must be 0
        self.kinetic_energy = 0
        return self.kinetic_energy


    def check_emit_electron(self, currentIntensity):
        # Check if electrons can be emitted based on kinetic energy and current intensity
        if self.kinetic_energy > 0 and currentIntensity > 0:
            self.emit_electrons = True
            return True
        else:
            self.emit_electrons = False
            return False


    def set_WF(self, WF):
        # Set work function of the metal
        self.metal_WF = WF

    def calc_current(self,threshold_energy , photon_obj, intensity):
        # Calculate current based on threshold energy, photon object, and intensity
        if self.kinetic_energy == 0:
            self.current = 0
        else:
            self.current = self.amps_to_picoamps((photon_obj.no_of_photons(intensity) * threshold_energy))
        return round(self.current,0)

    def min_max(self, x, min_x, max_x):
        # Normalise a value between a minimum and maximum range
        x_scaled = ((x - min_x)/(max_x - min_x))
        return x_scaled

    def amps_to_picoamps(self, amps):
        # Convert amperes to picoamperes
        return amps * 1e14  # Conversion factor for amperes to picoamperes
