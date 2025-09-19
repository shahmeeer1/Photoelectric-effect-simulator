# tkinter used to render gui
# LoginSystem is my own file

"""
Overriding of __new__ method used from Stackoverflow.
Lines: 123 - 126, 166 - 168
https://stackoverflow.com/a/1810367

"""

from LoginSystem import Login, Register
import tkinter


class gui():

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("")
        # centres windows in centre of screen
        window_width, window_height = 440, 440
        screen_width, screen_height = ((self.root.winfo_screenwidth() - window_width) // 2), (
                    (self.root.winfo_screenheight() - window_width) // 2)
        self.root.geometry('{}x{}+{}+{}'.format(window_width, window_height, screen_width, screen_height))
        # Windows cannot be resized or maximised
        self.root.resizable(False, False)
        self.root.configure(bg='#444E5D')
        self.Frame = tkinter.Frame(bg='#444E5D')

        # ===== text labels =====
        self.Main_Label = ""
        self.Button1_Label = ""
        self.Button2_Label = ""

        # ===== Button commands =====
        self.Button1Command = None
        self.Button2Command = None

    # Function to close window
    def close_gui(self):
        self.root.destroy()
        self.root.update()

    def Create_Page(self):
        # ===== Main Heading =====
        Main_label = tkinter.Label(
            self.Frame,
            text=self.Main_Label,
            bg='#444E5D',
            fg='#FFFFFF',
            font=('Arial', 30)
        )

        # ===== Username Heading =====
        username_label = tkinter.Label(
            self.Frame,
            text="Username",
            bg='#444E5D',
            fg='#FFFFFF',
            font=('Arial', 16)
        )

        # ===== Password Heading =====
        password_label = tkinter.Label(
            self.Frame,
            text="Password",
            bg='#444E5D',
            fg='#FFFFFF',
            font=('Arial', 16)
        )

        # ===== Username Entry =====
        self.username_entry = tkinter.Entry(
            self.Frame,
            font=('Arial', 16)
        )

        # ===== Password Entry =====
        self.password_entry = tkinter.Entry(
            self.Frame,
            show="*",
            font=('Arial', 16)
        )

        # ===== Buttons =====
        Button1 = tkinter.Button(
            self.Frame,
            text=self.Button1_Label,
            bg='#cdffff',
            font=('Arial', 16),
            command=self.Button1Command
        )

        Button2 = tkinter.Button(
            self.Frame,
            text=self.Button2_Label,
            bg='#cdffff',
            font=('Arial', 16),
            command=self.Button2Command
        )

        # ===== GRID POSITIONING =====
        # - Labels
        Main_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
        username_label.grid(row=1, column=0)
        password_label.grid(row=2, column=0, pady=10)
        # - Entries
        self.username_entry.grid(row=1, column=1, pady=10)
        self.password_entry.grid(row=2, column=1)
        # - Buttons
        Button1.grid(row=3, column=0, columnspan=2, )
        # Allows for button2 to be disabled if necessary
        if not self.Button2Command == None:
            Button2.grid(row=4, column=0, columnspan=2, pady=20)

        self.Frame.pack()
        self.root.mainloop()


# ===== Login Window Class =====
class LoginPage(gui):
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(LoginPage, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.



    def __init__(self):
        super().__init__()
        self.root.title("Login")
        self.Main_Label = "Login"
        self.Button1_Label = "Login"
        self.Button2_Label = "Register"
        self.Button1Command = self.login_button
        self.Button2Command = self.register_button

        # creates object from 'LoginSystem' File
        self.login_instance = Login()

        self.Create_Page()


    # ===== Login Button Functionality =====
    def login_button(self):
        success = False
        username = self.username_entry.get()
        password = self.password_entry.get()
        success = self.login_instance.validate(username, password)
        if success:
            self.CorrectUsername = username
            self.close_gui()


    # ===== Register Button Functionality =====
    def register_button(self):
        switch(self, 0)

    def LoginState(self):
        return 1, self.CorrectUsername

class Registration(gui):
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(Registration, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.

    def __init__(self):
        super().__init__()
        self.root.title("Register")
        self.Main_Label = "Register"
        self.Button1_Label = "Register"
        self.Button2_Label = "Back"
        self.Button1Command = self.register_action
        self.Button2Command = self.back
        self.register_instance = Register()
        self.Create_Page()

    def back(self):
        switch(self, 1)

    def register_action(self):
        success = False
        username = self.username_entry.get()
        password = self.password_entry.get()
        success = self.register_instance.create_account(username, password)
        if success:
            # switch to login window once registration is complete
            switch(self, 1)


# ===== Switch Between Windows =====
def switch(self, flip):
    # flip indicates login page(0) and register page(1)
    self.close_gui()  # closes current gui
    if flip == 0:
        registration_gui = Registration()
    elif flip == 1:
        Loginpage = LoginPage()
