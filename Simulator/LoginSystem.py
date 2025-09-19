# Author: Shahmeer Khalid

# external Libraries:  tkinter - messagebox, random, sqlite3, string
# messagebox from tkinter used to display errors
# random used to generate random numbers
# sqlite3 used for database
# string used to easily assign variables with ascii values. e.g lines 121


"""
Overriding of __new__ method used from Stackoverflow.
Lines:33 - 36
https://stackoverflow.com/a/1810367

"""



from tkinter import messagebox
import random
import sqlite3
import string


class User():
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(User, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.

    def __init__(self):
        self._username = ""
        self._password = ""
        self._hash = ""
        self._salt = ""

        # ===== Database Attributes =====
        self.conn = sqlite3.connect('SimData.db')
        self.c = self.conn.cursor()
    def close_db(self):
        self.c.close()
        self.conn.close()

    def username_lookup(self, username):
        # Parameterised Query to maintain code and protect against SQL Injection
        query = "SELECT username FROM credentials WHERE username = ?"
        self.c.execute(query, (username,))
        exists = self.c.fetchone()
        if exists:  # If the Username is already in use
            return True
        else:  # If the username is not in use
            return False

    # Used to Display error message pop ups
    def Errorbox(self, titles, error):
        messagebox.showerror(title=titles, message=error)

    def recursive_hash(self, new_password, password, shift, i):
        # --- Constants ---
        Alpha = "abcdefghijklmnopqrstuvwxyz"
        Lower = "tbphlmfsqgidrozeckyjunxwva"

        # Iterate through password 
        while i < len(password):
            # If character is alphabetic
            if password[i].isalpha():
                # Find position of character in Lower and add shift
                pos = Lower.index(password[i].lower()) + shift
                # Handle wrap - around if pos goes beyond 'z'
                if pos > 25:
                    pos -= 25
                # Append corresponding character from Alpha
                new_password += Alpha[pos]
                # Recursive call to process next character
                return self.recursive_hash(new_password, password, shift, i + 1)

            # If charcter is numeric digit
            elif password[i].isnumeric():
                sum = 0
                x = bin(int(password[i]))[2:]  # Convert digit to binary
                for _ in x:
                    sum = sum + int(password[i])
                sum += 27
                # Append sum to new password
                new_password += str(sum)
            # Recursive call to process next character
            return self.recursive_hash(new_password, password, shift, i + 1)

        # Return final password after all charcters processed
        return new_password

    def hash(self, passwordt, salt):
        # combine inputted password and salt
        password = passwordt + salt
        # Last digit of salt used for shift
        shift = int(salt[-1])
        new_password = ""
        # Recursively Hashed
        new_password = self.recursive_hash(new_password, password, shift, 0)
        return new_password


class Register(User):
    def __init__(self):
        super().__init__()

    def SetUsername(self, username):
        # Username validation process
        if username == "":
            self.Errorbox("Error", "You must enter a username!")
            return False
        # Check if username contains whitespaces
        if ' ' in username:
            self.Errorbox("Error", "Username cannot contain whitespace characters")
            return False
        # check if username already exists
        exists = self.username_lookup(username)
        if exists:
            self.Errorbox("Error", "Username Already Exists")
            return False
        # set username if valid
        self._username = username
        return True

    def SetPassword(self, password):
        # Password validation process

        # Check if password is empty
        if password == "":
            self.Errorbox("Error", "You must enter a password!")
            return False
        # Password should contain the following attributes
        upper = False
        lower = False
        digit = False
        symbol = False
        symbols = '@$!%*?&'

        # Check every letter of password
        for letter in password:
            if letter.isupper():
                upper = True
            elif letter.islower():
                lower = True
            elif letter.isdigit():
                digit = True
            elif letter in symbols:
                symbol = True

        if not (upper and lower and digit and symbol):
            self.Errorbox("Error",
                          "Password must be secure and contain at least: 1 symbol, 1 digit, 1 uppercase, and 1 lowercase letter")
            return False

        if len(password) < 8:
            self.Errorbox("Error", "Password must be at least 8 characters long")
            return False

        if ' ' in password:
            self.Errorbox("Error", "Password must not contain whitespaces")
            return False

        # If all checks pass, set the password
        self._password = password
        return True

    # Recuursively generate salt
    def gen(self, Nsalt, upper, lower, numbers, length):
        if len(Nsalt) < length:
            # Assign randomly selected characters to salt
            Nsalt += random.choice(upper + lower + numbers) + random.choice(lower) + random.choice(numbers)
            # Recursively call salt generation algorithm
            return self.gen(Nsalt, upper, lower, numbers, length)
        else:
            return Nsalt

    # Salt generated for hashing with password later on
    def generatesalt(self):
        upper = string.ascii_uppercase  # 'ABCDEFGH...'
        numbers = string.digits  # '01234...'
        lower = string.ascii_lowercase  # 'abcdefg...'
        length = 32  # length of salt
        Nsalt = ""
        Nsalt = self.gen(Nsalt, upper, lower, numbers, length)
        return Nsalt

    # Store credentials in database
    def StoreCreds(self):
        self._salt = self.generatesalt()
        self._hash = self.hash(self._password, self._salt)
        with self.conn:  # changes are immediately commited
            self.c.execute("INSERT INTO credentials (Username, Salt, Hash)VALUES (?,?,?)", (self._username, self._salt, self._hash))

    # Account Creation Manager
    def create_account(self, username, password):
        # If inputted username and passsword are valid
        if self.SetUsername(username) and self.SetPassword(password):
            self.StoreCreds()
            return True
        else:
            return False


class Login(User):
    def __init__(self):
        super().__init__()
        self._oldhash = ""
        self.UserID = None

    # Salt and Hash retrieved from record. Password is not stored in database
    def RetrieveData(self):
        query = "SELECT * FROM credentials WHERE username = ?"
        self.c.execute(query, (self._username,))
        result = self.c.fetchone()
        self._salt = result[2]
        self._oldhash = result[3]


    # Username input validation
    def EnterUsername(self, username):
        if username == "":
            self.Errorbox("Error", "You must enter a username!")
            return False
        exists = self.username_lookup(username)
        if exists:
            self._username = username
            return True
        else:
            self.Errorbox("Error", 'Incorrect username or password!')
            return False

    # Password input validation
    def EnterPassword(self, password):
        if password == "":
            self.Errorbox("Error", "You must enter a password!")
            return False
        self._password = password
        return True

    # Credentials Validation Manager
    def validate(self, username, password):

        if self.EnterUsername(username):  # If inputted username is valid
            if self.EnterPassword(password):  # If inputted password is valid

                # Retrieve existing Salt and Hash value
                self.RetrieveData()
                # Hash the inputted password using the existing Salt
                self._hash = self.hash(self._password, self._salt)

                # If new hash value matches existing hash value
                if self._hash == self._oldhash:
                    # User validated and granted access 
                    messagebox.showinfo(title="Access Granted", message="Welcome user.")
                    self.close_db()
                    return True

                # User Denied Access
                else:
                    self.Errorbox("Error", 'Incorrect username or password!')
                    return False
            else:
                self.Errorbox("Error", 'Incorrect username or password!')
                return False
        return False
