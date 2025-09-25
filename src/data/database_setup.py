import sqlite3

"""
sqlite3 library used for database management
"""


class database_setup:
    def __init__(self, ):
        try:
            # Establish connection to the database
            self.conn = sqlite3.connect('resources/db/SimData.db')
            self.c = self.conn.cursor()
            # Create tables and populate with initial data

            self.create_results()
            self.create_metals_table()
            self.populate_metals()
            # Close the database connection
            self.close_db()
            # Indicate successful setup
            self.setup = True
        except:
            print("error establishing connection to database or ceating table")
            # Indicate setup failure
            self.setup = False

    def Database_Status(self):
        # Check the status of the database setup
        if self.setup:
            return 1 # Database setup successful
        else:
            return 0 # Database setup failed


    # Create the results table if it doesn't exist. one table for all results
    def create_results(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS results (
                            ResultID INTEGER PRIMARY KEY AUTOINCREMENT,
                            MetalName TEXT NOT NULL,
                            Wavelength REAL,
                            Frequency REAL,
                            LightIntensity REAL,
                            KineticEnergy REAL,
                            Current REAL,
                            PhotonEnergy REAL,
                            FOREIGN KEY (MetalName) REFERENCES metals(MetalName)
                        )""")
            self.conn.commit()
        except:
            print("Error creating results table")

    def create_metals_table(self):
        # Create the metals table if it doesn't exist
        # This table stored critical information on each metal
        self.c.execute("""CREATE TABLE IF NOT EXISTS metals (
                           MetalName TEXT PRIMARY KEY,
                           Atomicnumber INTEGER,
                           Workfunction REAL,
                           Tfrequency REAL,
                           Twavelength REAL
                       )""")
        self.conn.commit()

    def populate_metals(self):
        # Properties of metals to be inserted into the database

        #  frequency: Thz, workfunction: eV, wavelength: nm
        metal_properties = {
            "Aluminium": {"frequency": 551.3, "Work_Function": 2.28, "Atomic_Number": 13, "Wavelength": 543.8},
            "Beryllium": {"frequency": 897, "Work_Function": 3.71, "Atomic_Number": 4, "Wavelength": 334.2},
            "Caesium": {"frequency": 517.4, "Work_Function": 2.14, "Atomic_Number": 55, "Wavelength": 579.4},
            "Calcium": {"frequency": 694, "Work_Function": 2.87, "Atomic_Number": 20, "Wavelength": 432.6},
            "Cobalt": {"frequency": 969.9, "Work_Function": 4.01, "Atomic_Number": 27, "Wavelength": 309.2},
            "Gold": {"frequency": 524.7, "Work_Function": 2.17, "Atomic_Number": 79, "Wavelength": 571.4},
            "Iron": {"frequency": 911.6, "Work_Function": 3.77, "Atomic_Number": 26, "Wavelength": 328.9},
            "Lead": {"frequency": 720.6, "Work_Function": 2.98, "Atomic_Number": 82, "Wavelength": 416.1},
            "Mercury": {"frequency": 880.1, "Work_Function": 3.64, "Atomic_Number": 80, "Wavelength": 340.6},
            "Sodium": {"frequency": 665, "Work_Function": 2.75, "Atomic_Number": 11, "Wavelength": 450.9},
            "Uranium": {"frequency": 945.4, "Work_Function": 3.91, "Atomic_Number": 92, "Wavelength": 317.1},
            "Zinc": {"frequency": 577.9, "Work_Function": 2.39, "Atomic_Number": 30, "Wavelength": 518.8},
        }

        try:
            # Clear existing data in metals table
            self.c.execute("DELETE FROM metals")
            # Insert metal properties into the metals table
            for metal, property in metal_properties.items():
                self.c.execute(
                    '''
                            INSERT INTO metals(MetalName, Atomicnumber, Workfunction, Tfrequency, Twavelength) 
                            VALUES (?,?,?,?,?)
                        ''',(metal, property["Atomic_Number"], property["Work_Function"], property["frequency"],property["Wavelength"]))
        except:
            pass

        self.conn.commit()


    def close_db(self):
        # Close the database connection
        self.c.close()
        self.conn.close()


# metals = ['Aluminium', 'Beryllium', 'Caesium', 'Calcium', 'Cobalt', 'Gold', 'Iron', 'Lead', 'Mercury', 'Sodium', 'Uranium', 'Zinc']