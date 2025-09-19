import sqlite3

"""
sqlite3 used for database management
"""

def SaveData(Metals, username):

    try:
        #   Create Database connection and cursor
        connect = sqlite3.connect('SimData.db')
        cursor = connect.cursor()

        #   Retrieve UserID from credentials table using username
        cursor.execute("SELECT UserID FROM credentials WHERE Username = ?", (username,))
        UserID = cursor.fetchone()[0]
        #   Store metal results in correct table
        #   List comprehension to remove empty elements from list
        for i in [metal for metal in Metals if metal != ""]:
            for result in i.results:
                ins = [UserID] + result
                query = """INSERT INTO {} 
                (UserID, Wavelength, Frequency, LightIntensity, KineticEnergy, Current, PhotonEnergy)
                VALUES(?,?,?,?,?,?,?)""".format(i.name)

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

