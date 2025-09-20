import pygame
import pygame_gui
import threading
import sqlite3
import buttons

"""
pygame and pygame_gui used for GUI
threading used for creating timer for button enabling and delay
line: 64

sqlite3 used for database management

# buttons is my own library

Overriding of __new__ method used from Stackoverflow.
Lines: 41 - 44
https://stackoverflow.com/a/1810367

"""


pygame.init()

# Return Button cass. Subclass of Buttons. Returns a value when clicked
class ReturnButton(buttons.Button):
    def __init__(self, x_ratio, y_ratio, width_ratio, height_ratio, image, surface_width, surface_height, return_obj):
        super().__init__(x_ratio, y_ratio, width_ratio, height_ratio, image, surface_width, surface_height)
        self.return_obj = return_obj

    def draw(self, surface):
        new_return = super().draw(surface)
        if new_return:
            return True, self.return_obj,
        else:
            return False, None

class ViewData:
    _instance = None  # Check if an instance of this class already exists

    # Singleton pattern initialiser
    def __new__(cls, screen):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(ViewData, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.

    def __init__(self, screen):
        #   Get screen dimensions
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w , info.current_h

        #   Create Game window
        self.screen = screen
        pygame.display.set_caption('View Data')

        #   Load and scale images
        self.Load_images()

        #   Draw Buttons
        self.CreateButtons()

        self.conn = sqlite3.connect('SimData.db')
        self.c = self.conn.cursor()


    def CreateButtons(self):

        self.quit_button = buttons.Button(0.038, 0.86, 0.1758, 0.095, self.images[1], self.WIDTH, self.HEIGHT)
        #   Disable buttons for 1 second1 to avoid miss-clicking using threading
        self.quit_button.DisableAll()
        threading.Timer(0.5, self.quit_button.EnableAll).start()

        # Create metal buttons
        self.buttons_list = [

            ReturnButton(0.0638, 0.0981, 0.186, 0.1126, self.images[2], self.WIDTH, self.HEIGHT, "Aluminium"),
            ReturnButton(0.3100, 0.0981, 0.186, 0.1126, self.images[3], self.WIDTH, self.HEIGHT, "Beryllium"),
            ReturnButton(0.5560, 0.0981, 0.186, 0.1126, self.images[4], self.WIDTH, self.HEIGHT, "Caesium"),

            ReturnButton(0.0638, 0.2449, 0.186, 0.1126, self.images[5], self.WIDTH, self.HEIGHT, "Calcium"),
            ReturnButton(0.3100, 0.2449, 0.186, 0.1126, self.images[6], self.WIDTH, self.HEIGHT, "Cobalt"),
            ReturnButton(0.5560, 0.2449, 0.186, 0.1126, self.images[7], self.WIDTH, self.HEIGHT, "Gold"),

            ReturnButton(0.0638, 0.3917, 0.186, 0.1126, self.images[8], self.WIDTH, self.HEIGHT, "Iron"),
            ReturnButton(0.3100, 0.3917, 0.186, 0.1126, self.images[9], self.WIDTH, self.HEIGHT, "Lead"),
            ReturnButton(0.5560, 0.3917, 0.186, 0.1126, self.images[10], self.WIDTH, self.HEIGHT, "Mercury"),

            ReturnButton(0.0638, 0.5380, 0.186, 0.1126, self.images[11], self.WIDTH, self.HEIGHT, "Sodium"),
            ReturnButton(0.3100, 0.5380, 0.186, 0.1126, self.images[12], self.WIDTH, self.HEIGHT, "Uranium"),
            ReturnButton(0.5560, 0.5380, 0.186, 0.1126, self.images[13], self.WIDTH, self.HEIGHT, "Zinc"),

            ReturnButton(0.0638, 0.6852, 0.186, 0.1126, self.images[14], self.WIDTH, self.HEIGHT, "ShowAll"),
            ReturnButton(0.3100, 0.6852, 0.186, 0.1126, self.images[15], self.WIDTH, self.HEIGHT, "DataInfo"),
            ReturnButton(0.5560, 0.6852, 0.186, 0.1126, self.images[16], self.WIDTH, self.HEIGHT, "MetalsInfo"),
        ]

        # Create pygame_gui manager
        self.manager = pygame_gui.UIManager((int(self.WIDTH), int(self.HEIGHT)), "Resources/Styling/ButtonTheme.JSON")

        # set dynamic button size
        buttons_size = (self.WIDTH * 0.0716, self.HEIGHT * 0.127)

        # Create 'SortBy' buttons and store in array
        self.FrequencyButton = pygame_gui.elements.UIButton(pygame.Rect((self.WIDTH * 0.847, self.HEIGHT * 0.193), buttons_size), "Frequency", manager=self.manager, object_id="#ViewData")
        self.KineticButton =  pygame_gui.elements.UIButton(pygame.Rect((self.WIDTH * 0.847, self.HEIGHT * 0.3507), buttons_size), "KineticE", manager=self.manager, object_id="#ViewData")
        self.PhotonButton = pygame_gui.elements.UIButton(pygame.Rect((self.WIDTH * 0.847, self.HEIGHT * 0.5081), buttons_size), "PhotonE", manager=self.manager, object_id="#ViewData")
        self.WorkfunctionButton = pygame_gui.elements.UIButton(pygame.Rect((self.WIDTH * 0.847, self.HEIGHT * 0.6655), buttons_size), "WorkF", manager=self.manager, object_id="#ViewData")

        self.sort_buttons = [self.FrequencyButton, self.KineticButton, self.PhotonButton, self.WorkfunctionButton]



    def Load_images(self):
        # Load images including background images and button images

        self.background_image = pygame.image.load('Resources/view data/MenuBackground.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        self.ButtonsRect_image = pygame.image.load('Resources/view data/ButtonsRect.png').convert_alpha()
        self.ButtonsRect_image = pygame.transform.scale(self.ButtonsRect_image, (self.WIDTH * 0.724, self.HEIGHT * 0.77))

        self.SortRect_image = pygame.image.load('Resources/view data/SortRect.png').convert_alpha()
        self.SortRect_image = pygame.transform.scale(self.SortRect_image, (self.WIDTH * 0.18, self.HEIGHT * 0.77))

        self.SortByTitle = pygame.image.load('Resources/view data/SortByTitle.png').convert_alpha()
        self.SortByTitle = pygame.transform.scale(self.SortByTitle, (self.WIDTH * 0.1569, self.HEIGHT * 0.095))

        self.ViewDataTitle = pygame.image.load('Resources/view data/ViewDataTitle.png').convert_alpha()
        self.ViewDataTitle = pygame.transform.scale(self.ViewDataTitle, (self.WIDTH * 0.2448, self.HEIGHT * 0.058))

        button_names = [
            "Advance.png", "Quit.png", "Aluminium.png",
            "Beryllium.png", "Caesium.png", "Calcium.png",
            "Cobalt.png", "Gold.png", "Iron.png", "Lead.png",
            "Mercury.png", "Sodium.png", "Uranium.png", "Zinc.png",
            "ShowAllButton.png", "DataInfoButton.png", "MetalsInfoButton.png"
        ]
        image_paths = ['Resources/Select Metals Images/SelectButtons/' + i for i in button_names]
        self.images = self.load_button_images(image_paths, 1)  # Load all images in list


    def load_button_images(self, image_paths, scale):
        # method to load button images
        scaled_images = []

        for path in image_paths:
            # load image
            img = pygame.image.load(path).convert_alpha()
            # scale image
            scaled_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            # Append to list
            scaled_images.append(scaled_img)
        return scaled_images

    def Retrieve_results(self, name):
        # Method to retrieve results for specific metal from appropriate table
        """
            This cross table query will select from the table with the name of the metal,
            the following values: wavelength, frequency, LightIntensity
            Kinetic Energy, Current and PhotonEnergy given that the
            UserID of the row in the metal table is the same as the
            UserID associated with the user's username stored in the
            credentials table.
        """
        # retrieve results for a specific metal
        query = """
                SELECT Wavelength, Frequency, LightIntensity,
                    KineticEnergy, Current, PhotonEnergy
                FROM results
                WHERE MetalNAme = ?
                """

        self.c.execute(query, (name,))
        data = self.c.fetchall()
        return data

    """NEEDS TO BE REWORKED"""
    def RetrieveAll(self):
        # Method to retrieve results for all metals from appropriate tables
        data = [] # initialise 2d array which will store data
        # List of metals

        """ 
            This loop will make a query to each of the 12 tables. It will retrieve the 
            following values: Wavelength, Frequency, LightIntensity, KineticEnergy, Current, PhotonEnergy
            from the table given that the UserID of the row in the metal table is the same as the 
            UserID associated with the user's username stored in the credentials table. this ensures that only the 
            Users data is retrieved from the database and no one else's. 
        """
        for metal in metals:
            query = """SELECT Wavelength, Frequency, LightIntensity, 
                               KineticEnergy, Current, PhotonEnergy 
                               FROM {} as m, credentials as c 
                               WHERE c.Username = ? and m.UserID = c.UserID;""".format(metal)
            self.c.execute(query, (self.Username,))
            data += self.c.fetchall()
        return data

    """Rework to avoid unnecessary db queries potentially?"""
    def ApproximatePlanckConstant(self, metal_name):
        # Method to approximate a value for plancks constant (6.63e-34) using their gathered data

        """
            This query retrieves the average value of the frequency column where the UserID associated
            with the username in the credentials table matches the UserId in the results row and that
            the value for current in that row is > 0
        """

        query = """SELECT AVG(frequency) 
                        FROM {} as m, credentials as c
                        WHERE current > 0 and c.Username = ? and m.UserID = c.UserID;""".format(metal_name)

        self.c.execute(query, (self.Username,))

        # store the retrieved value for average frequency from the query
        average_frequency = self.c.fetchone()[0]

        # This query has the same conditions as the previous query but instead returns the average of the photonEnergy column
        query = """SELECT AVG(PhotonEnergy) 
                        FROM {} as m, credentials as c
                        WHERE current > 0 and c.Username = ? and m.UserID = c.UserID;""".format(metal_name)
        self.c.execute(query, (self.Username,))
        average_energy = self.c.fetchone()[0]

        if average_energy is not None and average_frequency is not None:
            # If values were retrieved for average Frequency and photon energy calculate a value for Planks constant
            return str(round((((average_energy * 1.602e-19)/(average_frequency * 1e12)) * 1e34), 3)) + "e-34"
        else:
            return "None"

    """rework to updated database schema"""
    def RetrieveMetalData(self):
        # Method to retrieve data about the metals from the 'metals' table
        new_metal_data = []
        # This query returns the Name, AtomicNumber, WorkFunction, Tfrequency, Twavelength of every row
        self.c.execute("SELECT MetalName, AtomicNumber, WorkFunction, Tfrequency, Twavelength FROM metals")
        # query output is stored in 2d array
        metal_data = self.c.fetchall()
        for metal in metal_data:

            # This query counts the total number results for each metal

            query = ("""SELECT COUNT(*) 
                     FROM results as
                     WHERE MetalName = ?;""")
            self.c.execute(query, (metal[0],))

            results = list(metal)
            results.append(self.c.fetchone()[0])
            results.append(self.ApproximatePlanckConstant(metal[0]))
            # values for Planck's constant and row count added to metals data
            new_metal_data.append(results)
        return new_metal_data


    def merge(self, left, right, column):
        # Merge sort algorithm to sort a 2d array based on the values in a given column
        sorted = [] # empty list to store the sorted values
        leftpos = 0 # pointer for the left half of the array
        rightpos = 0 # pointer for the right half of the array

        while leftpos < len(left) and rightpos < len(right):
            if float(left[leftpos][column]) < float(right[rightpos][column]):
                # Compare left and right values in each sub array
                # Append the greater value to the sorted array
                sorted.append(left[leftpos])
                leftpos += 1 # move pointer to next left element
            else:
                sorted.append((right[rightpos]))
                rightpos += 1 # move pointer to next right element

        while rightpos < len(right):
            # Add any remaining elements in right half to sorted array
            sorted.append(right[rightpos])
            rightpos += 1 # move pointer to next right element

        while leftpos < len(left):
            # Add any remaining elements in the left half to sorte aray
            sorted.append(left[leftpos])
            leftpos += 1 # move pointer to next left element

        return sorted

    def merge_sort(self, data, column):
        # Part of merge sort algorithm
        # Array is recursively broken into sub arrys

        if len(data) <= 1:
            # If array contains one single value
            return data
        # Calculate centre of array
        centre = len(data) // 2
        # Slice the array into two sub arrays
        left_half = data[:centre]
        right_half = data[centre:]

        # Each half is recursively halved to single element lists then resorted
        left_half = self.merge_sort(left_half, column)
        right_half = self.merge_sort(right_half, column)

        # Merge the sorted halves back together
        return self.merge(left_half, right_half, column)



    def Display_Results(self, metal_name, SortBy):
        table_data = [] # list to hold table data

        #   Create Window for dispaying table
        window_rect = pygame.Rect(self.WIDTH * 0.065, self.HEIGHT * 0.1157, self.WIDTH * 0.846, self.HEIGHT * 0.463)
        window = pygame_gui.elements.UIWindow(window_rect, self.manager,window_display_title="Data Table")

        # Create a UIScrollingContainer to hold the table within the window
        scrolling_container = pygame_gui.elements.UIScrollingContainer(pygame.Rect((0, 0), window.get_container().get_size()),self.manager,container=window)

        # Column headings for the table
        headings = ["Wavelength", "Frequency", "Light\nIntensity", "KineticE", "Current", "PhotonE"]

        # metal_name is the return value for each button.
        # Determine what kind of table to display based on return value

        if metal_name in ["ShowAll", "DataInfo", "MetalsInfo"]:
            # --- Special Cases ---
            if metal_name == "ShowAll":
                # Display results for all metals
                table_data = self.RetrieveAll()

            elif metal_name == "MetalsInfo":
                # Display information about each metal
                table_data = self.RetrieveMetalData()
                # Update table headings appropriately
                headings = ["Name", "Atomic\nNumber", "WorkF", "Threshold\nFrequency", "Threshold\nWavelength", "Number of\nResults", "Calculated\nPlanck Const"]

            elif metal_name == "DataInfo":
                # Display information about the user
                table_data = self.RetrieveUserData()
                # Update table headings appropriately
                headings = ["Username", "UserId", "Total\nResults"]
        else:
            # --- standard case ---
            # display results for a single selected metal
            table_data = self.Retrieve_results(metal_name)

        if SortBy is not None:
            if metal_name == "DataInfo":
                pass
            # If the user has selected a button on how to sort the data
            elif metal_name == "MetalsInfo" and SortBy == "WorkF":
                # Merge sort retrieved data by using corresponding heading
                table_data = self.merge_sort(table_data, headings.index(SortBy))

            elif metal_name != "MetalsInfo" and SortBy != "WorkF":
                table_data = self.merge_sort(table_data, headings.index(SortBy))
            else:
                pass

        # Dimensions and position of table columns
        cell_width = self.WIDTH * 0.098
        cell_height = self.HEIGHT * 0.081
        table_x = self.WIDTH * 0.0326
        table_y = self.HEIGHT * 0.0579

        for index, cell in enumerate(headings):
            # dynamically create column heading textboxes
            cell_text_box = pygame_gui.elements.UITextBox(html_text=cell,
                                                          relative_rect=pygame.Rect((table_x + index * cell_width, table_y),(cell_width, cell_height)),
                                                          manager=self.manager,container=scrolling_container)

        # Dimensions of table rows
        table_y = self.HEIGHT * 0.139
        cell_height = self.HEIGHT * 0.0463

        for row_index, row in enumerate(table_data):
            # Dynamically create table rows
            for col_index, cell in enumerate(row):
                cell_text_box = pygame_gui.elements.UITextBox(html_text=str(cell),
                                                              relative_rect=pygame.Rect((table_x + col_index * cell_width, table_y + row_index * cell_height),(cell_width, cell_height)),
                                                              manager=self.manager,container=scrolling_container)

        # Calculate dimensions of scrolling container required
        height = cell_height * len(table_data) + (self.HEIGHT * 0.231)
        length = cell_width * len(headings) + (self.WIDTH * 0.0326)
        # Update dimensions of scrolling container
        scrolling_container.set_scrollable_area_dimensions((length, height))
        # Set the window to blocking to limit user interaction with buttons below window
        window.set_blocking(True)
        # Temporarily disable all buttons on page whilst window is open
        self.quit_button.DisableAll()

    def RetrieveUserData(self):
        total = 0 # variable to store the total number of results
        metals = ['Aluminium', 'Beryllium', 'Caesium', 'Calcium', 'Cobalt', 'Gold', 'Iron', 'Lead', 'Mercury', 'Sodium', 'Uranium', 'Zinc']
        # Iterate through the list of metals
        for metal in metals:
            # SQL query to count the total number of results for the current metal and the current user
            query = ("""SELECT COUNT(*)
                    FROM {} as m, credentials as c
                    WHERE c.Username = ? and m.UserID = c.UserID;""").format(metal)

            self.c.execute(query, (self.Username,))
            # Fetch the result of the query and add it to the total
            total += int(self.c.fetchone()[0])

        # retrieve the UserId from the credentials table
        userid = self.c.execute("SELECT UserID FROM credentials WHERE Username = ?", (self.Username,)).fetchone()[0]
        # Add the user data to the results array
        results = [[self.Username, str(userid), str(total)]]
        return results




# Method for creating GUI and controlling interactions
    def draw_page(self):
        # Initialise pygame clokc

        # Define position for static GUI elements
        clock = pygame.time.Clock()
        ButtonsRect_pos = ((self.WIDTH * 0.04), (self.HEIGHT * 0.06))
        SortRect_pos = ((self.WIDTH * 0.8), (self.HEIGHT * 0.064))
        SortByTitle_pos = ((self.WIDTH * 0.809), (self.HEIGHT * 0.0914))
        ViewDataTitle_pos = ((self.WIDTH * 0.2806), 0)

        SortBy = None # Variable to store current sorting option

        # --- Main Loop ---
        while True:
            delta_time = clock.tick(60) / 1000.0 # Calculate time elapsed since last frame
            # Draw background GUI elements
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.ButtonsRect_image, ButtonsRect_pos)
            self.screen.blit(self.SortRect_image, SortRect_pos)
            self.screen.blit(self.SortByTitle, SortByTitle_pos)
            self.screen.blit(self.ViewDataTitle, ViewDataTitle_pos)

            # Quit button
            quit = self.quit_button.draw(self.screen)

            # Check if quit button clicked
            if quit:
                # Return to Menu
                return 1

            for i in self.buttons_list:
                # Draw metal and other buttons in buttons_list array
                clicked, return_obj = i.draw(self.screen)
                if clicked:
                    # Display the results of the clicked button
                    self.Display_Results(return_obj, SortBy)

            # --- Process Events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit pygame when exit button clicked
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Mouse click logic
                    left_button_down = False



                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element in (self.FrequencyButton, self.KineticButton, self.WorkfunctionButton, self.PhotonButton):
                        # Check which sorting button is pressed
                        for i in self.sort_buttons:
                            # If sort button clicked
                            if i.check_pressed():
                                # Disable selected sorting button
                                i.disable()
                                SortBy = i.text
                            else:
                                # Enable other sorting buttons
                                i.enable()
                elif event.type == pygame_gui.UI_WINDOW_CLOSE:
                    # Enable all buttons if a UI window is closed
                    self.quit_button.EnableAll()


        # --- Update and draw Pygame GUI elements on the screen ---
                self.manager.process_events(event)

            self.manager.update(delta_time)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
