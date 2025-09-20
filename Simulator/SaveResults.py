import sqlite3

"""
sqlite3 used for database management
"""

def SaveData(Metals):

    try:
        #   Create Database connection and cursor
        connect = sqlite3.connect('Simulator/SimData.db')
        cursor = connect.cursor()

        #   List comprehension to remove empty elements from list
        for metal in [metal for metal in Metals if metal != ""]:
            for result in metal.results:
                ins = [metal.name] + result
                query = """INSERT INTO results 
                (MetalName, Wavelength, Frequency, LightIntensity, KineticEnergy, Current, PhotonEnergy)
                VALUES(?,?,?,?,?,?,?)"""

                cursor.execute(query, ins)

        connect.commit()

    except sqlite3.Error as e:
        print("SQLite error:", e)
        print("ERROR IN SAVERESULTS")

    finally:
        #   Close database
        if cursor:
            cursor.close()
        if connect:
            connect.close()
        return 1

