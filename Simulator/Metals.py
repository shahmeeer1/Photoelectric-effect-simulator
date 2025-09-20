import sqlite3

"""

Overriding of __new__ method similar to one from Stackoverflow.
Lines: 15 - 22
https://stackoverflow.com/a/1810367
"""


class Metal:
    # ===== class variables =====
    _instances = {} # Dictionary to store instances of Metal class
    _instantiated = False # Flag to track if the class has been instantiated

    # Singleton pattern to ensure only one object for each metal created
    def __new__(cls, name):
        # Check if an instance for the metal name already exists
        if name not in cls._instances:
            # If not, create a new instance and store it in the _instances dictionary
            instance = super(Metal, cls).__new__(cls)
            cls._instances[name] = instance # Store the instance in the dictionary
        return cls._instances[name]

    def __init__(self, name):
        # Initialize properties of the metal object if not already initialised
        if not hasattr(self, 'instantiated'):
            self.name = name
            self.Atomic_Number, self.Work_Function, self.Tfrequency, self.Twavelength = self.setup_metal()
            self.results = [] # Results obtained form simulation
            self.instantiated = True


    def setup_metal(self):
        try:
            # Establish connection to the SQLite database
            connect = sqlite3.connect('Simulator/SimData.db')
            c = connect.cursor()
            # Query database to retrieve metal properties based on name
            query = "SELECT Atomicnumber, Workfunction, Tfrequency, Twavelength FROM metals WHERE MetalName = ?"
            c.execute(query, (self.name,))
        except:
            # Handle error if unable to setup metal
            print("Error setting up metal.")
            print("Metal name: {}".format(self.name))
        
        # Fetch results from the database query
        results = c.fetchone()
        return results

    """ seperation of concerns. need to remove"""
    def check_emit_electrons(self, photon_enery):
        # Check if the given photon energy is sufficient to emit electrons from the metal
        # In order to emit electrons, the photon energy must be greater than the threshold energy
        # which is also known as the 'work function' of the metal
        if photon_enery >= self.Work_Function:
            return True
        else:
            return False

    def get_name(self):
        # Return the name of the metal
        return self.name

    def get_Work_Function(self):
        # Return the work function of the metal
        return self.Work_Function

    def get_Tfrequency(self):
        # Return the threshold frequency of the metal
        return self.Tfrequency

    def get_Twavelength(self):
        # Return the threshold wavelength of the metal
        return self.Twavelength