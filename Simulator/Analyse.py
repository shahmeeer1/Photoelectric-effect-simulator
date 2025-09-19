import pygame
import pygame_gui
import sqlite3
import buttons
"""
pygame and pygame_ui library used for gui
sqlite3 used for database management

# buttons is my own file


some of the Overriding of __new__ method used from Stackoverflow.
https://stackoverflow.com/a/1810367
Lines: 716 - 710
"""
pygame.init()


class Regression:
    # Constructor to initialize Regression object with experimental data
    def __init__(self, results):
        self.results = results
        # Stores sum of x and y values from results (Σx and Σy)
        self.Sum_x, self.Sum_y = self.__sum_x_and_y()
        # Stores sum of products of x and y values from results Σ(xy)
        self.Sum_xy = self.__sum_xy()
        #   Stores sum of squared x values from results Σ(x^2)
        self.Sum_x_squared = self.__sum_x_squared()
        #   Stores gradient of the regression line
        self.Gradient = self.__CalculateGradient()
        #   y-intercept of the regression line
        self.Intercept = self.__CalculateIntercept()
        #   Stores coordinates of regression line
        self.LineCoords = []

    def __sum_x_and_y(self):
        # Private method to calculate sum of x and y values from results
        Sum_x = 0
        Sum_y = 0
        for x, y in self.results:
            Sum_x += x
            Sum_y += y
        return Sum_x, Sum_y

    def __sum_xy(self):
        # Private method to calculate sum of products of x and y values from results
        xy = 0
        for x, y in self.results:
            xy += x * y
        return xy

    def __sum_x_squared(self):
        # Private method to calculate sum of squared x values from results
        x_squared = 0
        for i in self.results:
            x_squared += i[0] ** 2
        return x_squared

    def __CalculateGradient(self):
        # Private method to calculate gradient
        try:
            Gradient = round(((len(self.results) * self.Sum_xy) - (self.Sum_x * self.Sum_y)) / (
                    (len(self.results) * self.Sum_x_squared) - (self.Sum_x) ** 2), 2)
            #   Gradient = (N * Σxy - Σx * Σy) / (N * Σx² - (Σx)²)
            #   Where N is the number of coordinates, x and y are the x and y coordinates of each point respectively
        except:
            # Handling division by zero error
            Gradient = 0
        return Gradient

    def __CalculateIntercept(self):
        try:
            # Private method to calculate y-intercept of the regression line
            Intercept = (self.Sum_y - (self.Gradient * self.Sum_x)) / len(self.results)
            # Y intercept = (Σy * Σx² - Σx * Σxy) / (n * Σx² - (Σx)²)
            return Intercept
        except:
            # Handling divsion by zero error
            return 0
    def draw_line(self, graph_surface, left_coordinate, right_coordinate, Cutoff, *args):
        try:
            # Method to draw the regression line on a graph surface
            # Also calculates y-coordinate of right end of line based on gradient and right coordinate

            y_coord = (self.Gradient * right_coordinate) + self.Intercept

            # Check if line is cut off
            if Cutoff:

                # Calculate x-coordinate of intersection point with cutoff line
                x_int = (args[0] - self.Intercept) / self.Gradient

                # Store coordinates of line endpoints with rounding
                self.LineCoords = [[round(x_int, 2), round(args[0], 2)], [round(right_coordinate, 2), round(y_coord, 2)]]
            else:
                # Store coordinates of line endpoints with rounding ( without cutoff )
                self.LineCoords = [[round(left_coordinate, 2), round(self.Intercept, 2)],
                                   [round(right_coordinate, 2), round(y_coord, 2)]]
            # Draw line on graph surface
            pygame.draw.line(graph_surface, "black", self.LineCoords[0], self.LineCoords[1], 4)
            return True
        except:
            return False

class Graph:
    _instances = []  # Class attribute to store instances; 2D array
    _instantiated = False  # Flag indicating whether instances have been created

    """
    Custom constructor to control instantiation of objects. Follows singleton pattern.
    Allows for only 4 distinct instances of this or any subclass of this class.
    For every metal, there can be up to 4 (and no more than 4) associated objects which only need to be instantiated once.
    """

    def __new__(cls, metal, graph, username):
        for i in cls._instances:  # Iterates through class method _instances
            if i[0] == metal:  # Checks if any instances associated with this metal already exist
                for k in range(1, len(i)):
                    if i[k].name == graph:  # Checks if an object for the current graph already exists
                        return i[k]  # Returns pre-existing object
                new_graph = super().__new__(cls)  # Creates new object
                new_graph.name = graph  # Assigns argument value to object 'name' attribute
                i.append(new_graph)  # new object added to class variable array
                return new_graph  # returns new object
        new_instance = super().__new__(cls)  # Creates first object associated with this metal
        new_instance.name = graph  # assigns object 'name' attribute.
        cls._instances.append(
            [metal, new_instance])  # Adds record of object associated with this metal to class variable
        return new_instance

    #   Continued from custom initialiser
    def __init__(self, metal, graph, username):
        if not hasattr(self, 'metal'):  # Check if attributes are already initialized
            self.metal = metal
            self.metal = metal
            self.name = graph
            self.results = []
            self.coords = []
            self.Username = username

            # Optimisation Attributes
            self.Drawn = False

            # Retrieve window dimensions
            info = pygame.display.Info()
            self.WIDTH, self.HEIGHT = info.current_w, info.current_h

            # Connect to database
            self.conn = sqlite3.connect('Credentials.db')
            self.c = self.conn.cursor()
            self.font = pygame.font.Font(None, int(self.WIDTH * 38 / 1536))

            # Setup graph surface
            self.SetupGraphSurface()

    # Methods to scale values to fit the screen
    def Ratio_t(self, tup):
        # Base window size was 1536, 864 pixels during development thus scale must be a ration of this
        return round((self.WIDTH * tup[0]) / 1536, 2), round((self.HEIGHT * tup[1]) / 864, 2)

    # Method to calculate coordinates based on results
    # To be overridden in subclass
    def CalculateCoordinates(self):
        self.coords = []
        try:
            # Check if results were found
            if len(self.results) == 0:
                return False
            else:
                return True
        except:
            return False

    # Method to display the graph surface on the screen
    def DisplayGraph(self, screen, pos):
        screen.blit(self.GraphSurface, pos)

    # Method to get the graph surface
    def GetSurface(self):
        return self.GraphSurface

    # Method to setup the graph surface
    def SetupGraphSurface(self):
        self.GraphSurface = pygame.Surface((self.WIDTH * 0.4, self.HEIGHT * 0.65))
        self.GraphSurface.fill((0, 255, 255))

    # Method to display loading message on graph surface
    def LoadingGraph(self):
        self.GraphSurface.fill((0, 255, 255))
        text_surface = self.font.render("LOADING\n GRAPH", True, "black", )
        self.GraphSurface.blit(text_surface, self.Ratio_t((270, 250)))

    # Method to display no results message on graph surface
    def NoResultsError(self):
        self.GraphSurface.fill((0, 255, 255))
        text_surface = self.font.render("NO RESULTS TO\n   DISPLAY", True, "black", )
        self.GraphSurface.blit(text_surface, self.Ratio_t((230, 250)))

    # Method to retrieve data from database
    def RetrieveData(self, param1, param2, username, *args):
        query = """SELECT {}, {}
                FROM {} as m, credentials as c
                WHERE c.Username = ? and c.UserID = m.UserID""".format(param1, param2, self.metal)
        self.c.execute(query, (username,))
        results = self.c.fetchall()
        return results

    # Abstract method for drawing graoph axes
    def EmptyGraphAxis(self):
        pass


# Method for Kinetic Energy against Frequency graph
# Subclass of graph class
class KE_VS_F(Graph):
    def __init__(self, metal, graph_type, username):
        super().__init__(metal, graph_type, username)

    # Method to draw empty graph axes
    def EmptyGraphAxis(self):
        self.GraphSurface.fill((0, 255, 255))

        #   y axis
        self.y = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        text_surface = self.font.render("Kinetic Energy", True, "black")
        rotated_text = pygame.transform.rotate(text_surface, 90)
        self.GraphSurface.blit(rotated_text, self.Ratio_t((20, 255)))

        #   x axis
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 270)), self.Ratio_t((550, 270)), 6)
        text_surface = self.font.render("Frequency (THz)", True, "black")
        self.GraphSurface.blit(text_surface, self.Ratio_t((270, 510)))

        #   arrows
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((544, 249)), self.Ratio_t((558, 271)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((558, 271)), self.Ratio_t((544, 293)), 6)

        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((29, 43)), self.Ratio_t((51, 27)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((51, 27)), self.Ratio_t((73, 43)), 6)

    # Method to calculate coordinates for drawing points on graph
    def CalculateCoordinates(self):
        # calls parent implementation of method
        S = super().CalculateCoordinates()
        if not S:  # if not empty
            return False

        self.y = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 270)), self.Ratio_t((550, 270)), 6)
        self.GraphSurface.fill((0, 255, 255))

        for i in self.results:  # iterates through results
            y_value, x_value = float(i[0]), int(i[1])  # unpacks data
            max_y, max_x = 2, 1000  # max and minimum values for x and y axis. based on simulator
            min_y = -2  # y axis has negative quadrant
            y_axis_length, x_axis_length = self.y.size[1], self.x.size[0]

            #   padding from left to right and bottom to top
            x_padding, y_padding = self.y.left, self.y.top
            x_coord = (x_value * (x_axis_length / max_x)) + x_padding  # x value calculated through scaling

            scale_factor = y_axis_length / (max_y - min_y)
            y_coord = y_padding + (max_y - y_value) * scale_factor  # y value calcualted throuhg scaling

            self.coords.append([x_coord, y_coord])

        return True

    def DrawGraph(self):
        count = 0
        # Method to draw graph
        for point in self.coords:  # plots coordinates
            count += 1
            pygame.draw.circle(self.GraphSurface, "black", (point[0], point[1]), 4)
        # Draws line of best fit using regression algorithm
        if count <= 1:
            return False
        Line = Regression(self.coords)
        drawn = Line.draw_line(self.GraphSurface, self.x.topleft[0], self.x.topright[0], True, self.y.bottomright[1])
        return drawn

    # Method to retrieve data from database
    def RetrieveData(self, param1, param2, username, *args):

        param1 = "KineticEnergy"  # Replaced with the fixed parameters
        param2 = "Frequency"

        #   This graph is only dependent on 2 variables so parent implementation is sufficient with slight changes
        results = super().RetrieveData(param1, param2, self.Username)
        results = [i for i in results if round(i[0], 2) > 0.00]
        if results:
            return results
        else:
            self.NoResultsError()


# class for Current against Light intensity graph
class I_vs_i(Graph):
    def __init__(self, metal, graph_type, username):
        super().__init__(metal, graph_type, username)

    # Method to draw emoty axis
    def EmptyGraphAxis(self):

        self.GraphSurface.fill((0, 255, 255))

        #   X axis
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 500)), self.Ratio_t((550, 500)), 6)
        text_surface = self.font.render("Light Intensity", True, "black")
        self.GraphSurface.blit(text_surface, self.Ratio_t((270, 510)))

        #   Y axis
        self.y = pygame.draw.line(self.GraphSurface, "black", self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        text_surface = self.font.render("Current (pA)", True, "black")
        rotated_text = pygame.transform.rotate(text_surface, 90)
        self.GraphSurface.blit(rotated_text, self.Ratio_t((20, 240)))

        #   Arrows
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((544, 479)), self.Ratio_t((558, 501)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((558, 501)), self.Ratio_t((544, 523)), 6)

        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((29, 43)), self.Ratio_t((51, 27)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((51, 27)), self.Ratio_t((73, 43)), 6)

    # method to calcualte coordinates
    def CalculateCoordinates(self):
        # x and y coordinates calculated through scaling data onto  axis
        S = super().CalculateCoordinates()
        if not S:
            # if not data retrieved
            return False
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 500)), self.Ratio_t((550, 500)), 6)
        self.y = pygame.draw.line(self.GraphSurface, "black", self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        self.GraphSurface.fill((0, 255, 255))

        for i in self.results:  # iterates through data
            y_value, x_value = float(i[0]), int(i[1])  # unpacks data
            max_y, max_x = 1000, 100  # max y and x axis values

            y_axis_length, x_axis_length = self.y.size[1], self.x.size[0]
            x_padding, y_padding = self.y.left, self.y.top

            # Coordinate calcualtions
            x_coord = (x_value * (x_axis_length / max_x)) + x_padding

            scale_factor = y_axis_length / max_y
            y_coord = self.GraphSurface.get_height() - ((y_value * scale_factor) + y_padding)

            # coordinates added to coordinate method
            self.coords.append([x_coord, y_coord])
        return True

    # Method to draw graph
    def DrawGraph(self):
        count = 0
        # coordinate of bottom of y axis
        min_y = self.y.bottomright
        for point in self.coords:
            # Only plots points above x-axis
            # Y coordinates in pygame are flipped thus the 'greater than' sign rather than 'lass than' sign
            if point[1] > min_y[1]:
                continue
            # plots points
            pygame.draw.circle(self.GraphSurface, "black", (point[0], point[1]), 4)
            count += 1
        # Draws regression line using regression algorithm
        if count <= 1:
            return False
        Line = Regression(self.coords)
        drawn = Line.draw_line(self.GraphSurface, self.x.topleft[0], self.x.topright[0], True, self.y.bottomright[1])
        return drawn

    # Retireves data from class
    def RetrieveData(self, param1, param2, username, *args):
        self.results = []
        param1 = "Current"
        param2 = "LightIntensity"
        username = self.Username

        """ 
             The current vs light Intensity graph is dependent on 3 factors; Current, 
             Light Intensity and Frequency. Variation in Frequency causes variations
             the 2 plotted quantities thus only data recorded with a constant Frequency
             can be plotted together. Due to this we must process the data to only
             include data recorded with the same Frequency.
             
             This aggregate SQL query selects Current and Light Intensity values
             from the table with the same name as the selected metal, where the 
             UserID for the record  in the metal table matches the UserID of the 
             current user in the credentials table, the values are greater 
             than 0 and there are atleast 3 or more results. The retrieved values 
             are grouped by Frequency and the most common Frequency is selected and 
             those values are returned
        """

        query = """SELECT m.Current, m.LightIntensity
                           FROM {} AS m
                           JOIN credentials AS c ON m.UserID = c.UserID
                           WHERE c.Username = ?
                               AND m.Frequency = (
                                   SELECT Frequency
                                   FROM {} AS m2
                                   JOIN credentials AS c2 ON m2.UserID = c2.UserID
                                   WHERE c2.Username = ? AND m2.Current > 0 AND m2.LightIntensity > 0
                                   GROUP BY m2.Frequency
                                   HAVING COUNT(*) > 2
                                   ORDER BY COUNT(*) DESC
                                   LIMIT 1
                               )""".format(self.metal, self.metal)

        self.c.execute(query, (username, username))

        results = self.c.fetchall()
        # Anomalous results are filtered out
        results = [i for i in results if round(i[0], 2) > 0.00]

        # Checks if there are any results left after processing
        if results:
            return results
        else:
            self.NoResultsError()
        #   display error on graph screen


# Class for graph of Kinetic Energy against Light Intensity
class KE_vs_i(Graph):
    def __init__(self, metal, graph_type, username):
        super().__init__(metal, graph_type, username)

    # method for empty axis
    def EmptyGraphAxis(self):

        self.GraphSurface.fill((0, 255, 255))

        #   X axis
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 500)), self.Ratio_t((550, 500)), 6)
        text_surface = self.font.render("Light Intensity", True, "black")
        self.GraphSurface.blit(text_surface, self.Ratio_t((270, 510)))

        #   Y axis
        self.y = pygame.draw.line(self.GraphSurface, "black", self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        text_surface = self.font.render("Kinetic Energy (J)", True, "black")
        rotated_text = pygame.transform.rotate(text_surface, 90)
        self.GraphSurface.blit(rotated_text, self.Ratio_t((20, 240)))

        #   Arrows
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((544, 479)), self.Ratio_t((558, 501)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((558, 501)), self.Ratio_t((544, 523)), 6)

        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((29, 43)), self.Ratio_t((51, 27)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((51, 27)), self.Ratio_t((73, 43)), 6)

    # Overridden method for calculating coordinates
    def CalculateCoordinates(self):
        S = super().CalculateCoordinates()
        if not S:
            # Checks if results found
            return False
        self.y = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 270)), self.Ratio_t((550, 270)), 6)
        self.GraphSurface.fill((0, 255, 255))

        for i in self.results: # iterates through data
            y_value, x_value = float(i[0]), int(i[1])
            max_y, max_x = 2, 100

            y_axis_length, x_axis_length = self.y.size[1], self.x.size[0]
            x_padding, y_padding = self.y.left, self.y.top

            # calculates coordinates using scalling onto axis
            x_coord = (x_value * (x_axis_length / max_x)) + x_padding

            scale_factor = y_axis_length / max_y
            y_coord = self.GraphSurface.get_height() - ((y_value * scale_factor) + y_padding)

            # calculated coordinates added to coordinates list attribute
            self.coords.append([x_coord, y_coord])
        return True

    # Method to draw graph
    def DrawGraph(self):
        count = 0
        min_y = self.y.bottomright
        for point in self.coords:
            # only plots points above x-axis
            if point[1] > min_y[1]:
                continue
            pygame.draw.circle(self.GraphSurface, "black", (point[0], point[1]), 4)
            count += 1
        # Draws regression line using regression algorithm
        if count <= 1:
            return False
        Line = Regression(self.coords)
        drawn = Line.draw_line(self.GraphSurface, self.x.topleft[0], self.x.topright[0], False)
        return drawn

    # Retrieve data from database
    def RetrieveData(self, param1, param2, username, *args):
        self.results = []
        param1 = "KineticEnergy"
        param2 = "LightIntensity"
        username = self.Username

        """ 
             The Kinetic Energy vs light Intensity graph is dependent on 3 factors; 
             Kinetic Energy, Light Intensity and Frequency. Variation in Frequency causes 
             variations the 2 plotted quantities thus only data recorded with a constant 
             Frequency can be plotted together. Due to this we must process the data to only
             include data recorded with the same Frequency.

             This aggregate SQL query selects KE and Light Intensity values
             from the table with the same name as the selected metal, where the 
             UserID for the record  in the metal table matches the UserID of the 
             current user in the credentials table, the values are greater 
             than 0 and there are at least 3 or more results. The retrieved values 
             are grouped by Frequency and the most common Frequency is selected and those values are returned
        """


        query = """SELECT m.KineticEnergy, m.LightIntensity
                           FROM {} AS m
                           JOIN credentials AS c ON m.UserID = c.UserID
                           WHERE c.Username = ?
                               AND m.Frequency = (
                                   SELECT Frequency
                                   FROM {} AS m2
                                   JOIN credentials AS c2 ON m2.UserID = c2.UserID
                                   WHERE c2.Username = ? AND m2.KineticEnergy > 0 AND m2.LightIntensity > 0
                                   GROUP BY m2.Frequency
                                   HAVING COUNT(*) > 2
                                   ORDER BY COUNT(*) DESC
                                   LIMIT 1
                                )

                               """.format(self.metal, self.metal)

        self.c.execute(query, (username, username))

        results = self.c.fetchall()
        # Filters out anomalous results
        results = [i for i in results if round(i[0], 2) > 0.00 and i[1] > 0.00]

        # Checks if there are any results left after processing and filtering data
        if results:
            return results
        else:
            self.NoResultsError()
        #   display error on graph screen


# Class for Current against Frequency graph
class I_vs_F(Graph):
    def __init__(self, metal, graph_type, username):
        super().__init__(metal, graph_type, username)

    # method for drawing empty graph axis
    def EmptyGraphAxis(self):

        self.GraphSurface.fill((0, 255, 255))

        #   X axis
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 500)), self.Ratio_t((550, 500)), 6)
        text_surface = self.font.render("Frequency (THz)", True, "black")
        self.GraphSurface.blit(text_surface, self.Ratio_t((270, 510)))

        #   Y axis
        self.y = pygame.draw.line(self.GraphSurface, "black", self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        text_surface = self.font.render("Current (pA)", True, "black")
        rotated_text = pygame.transform.rotate(text_surface, 90)
        self.GraphSurface.blit(rotated_text, self.Ratio_t((20, 240)))

        #   Arrows
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((544, 479)), self.Ratio_t((558, 501)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((558, 501)), self.Ratio_t((544, 523)), 6)

        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((29, 43)), self.Ratio_t((51, 27)), 6)
        pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((51, 27)), self.Ratio_t((73, 43)), 6)

    # method to remove vertical clusters from data
    def ProcessData(self):
        """
            Data involving Current and Frequency tends to produce vertical data sets.
            Variations in light Intensity lead to an increase in current across all
            values of frequency, resulting in vertical lines on the graph.
            The purpose of this graph is to show the general trend which occurs when Frequency
            is carried thus the vertical data sets can be processed to fit the trend and avoid
            wasted results or False conclusions.
        """

        # 2D array to store occurrences of x-coordinates.
        # Forms 3xn Matrix where n is the number of results
        Occurence_matrix = []

        for item in self.coords: # iterate through each coordinate
            add = True
            # Check if the x-coordinate is already in the matrix
            for unique in Occurence_matrix:
                if item[0] == unique[0]:
                    add = False
                    # If it's a repeated x-coordinate, update the total y-value and occurrence count
                    unique[1] += item[1]
                    unique[2] += 1
                    break
            # If it's a new x-coordinate, add it to the matrix
            if add:
                Occurence_matrix.append([item[0], item[1], 1])

        # Calculate the average y-value for each x-coordinate with more than 2 occurrences
        for row in Occurence_matrix:
            if row[2] > 2:
                row[1] = round(row[1] / row[2], 1)

        # Remove the occurrence count from each row of the matrix to form processed set of data
        for i in Occurence_matrix:
            i.pop(-1)
        return Occurence_matrix

    # calculate coordinates
    def CalculateCoordinates(self):
        S = super().CalculateCoordinates()
        if not S:
            # checks if results were found
            return False
        self.y = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((50, 35)), self.Ratio_t((50, 500)), 6)
        self.x = pygame.draw.line(self.GraphSurface, (0, 0, 0), self.Ratio_t((48, 270)), self.Ratio_t((550, 270)), 6)
        self.GraphSurface.fill((0, 255, 255))

        for i in self.results:
            y_value, x_value = float(i[0]), int(i[1])
            max_y, max_x = 1000, 1000

            y_axis_length, x_axis_length = self.y.size[1], self.x.size[0]
            x_padding, y_padding = self.y.left, self.y.top

            # coordinates calculated using scalling
            x_coord = (x_value * (x_axis_length / max_x)) + x_padding

            scale_factor = y_axis_length / max_y
            y_coord = self.GraphSurface.get_height() - ((y_value * scale_factor) + y_padding)

            self.coords.append([round(x_coord, 1), round(y_coord, 1)])
        # coordinates are processed to remove vertical data groups
        self.coords = self.ProcessData()

        min_y = self.y.bottomright[1]
        temp = self.coords
        self.coords = []
        for point in temp:
            # Points below the x-axis are removed
            if point[1] > min_y:
                continue
            else:
                self.coords.append(point)

        # checks if any coordinates still left after processing and filtering
        if len(self.coords) <= 1:
            return False

        temp = self.coords
        self.coords = []
        for i in temp:
            # Removes redundant coordinates
            if i not in self.coords:
                self.coords.append(i)

        return True

    # method to draw graph
    def DrawGraph(self):
        count = 0
        min_y = self.y.bottomright
        for point in self.coords:
            if point[1] > min_y[1]:
                # ensures that points below the x-axis are not plotted
                continue
            pygame.draw.circle(self.GraphSurface, "black", (point[0], point[1]), 4)
            count += 1
        # line of best fit drawn using regression algorithm
        if count <= 1:
            return False
        Line = Regression(self.coords)
        drawn = Line.draw_line(self.GraphSurface, self.x.topleft[0], self.x.topright[0], False)
        return drawn

    # Data retrieved from database
    def RetrieveData(self, param1, param2, username, *args):
        self.results = []
        param1 = "Current"
        param2 = "Frequency"
        username = self.Username

        """
            This query retrieves data for Current and Frequency from the database where 
            the UserID of the user matches the userID in the record and all retrieved values 
            are greater than 0
        """

        query = """Select m.Current, m.Frequency
                    FROM {} as m
                    JOIN credentials AS c ON m.UserID = c.UserID
                    WHERE c.Username = ?
                    AND m.Current > 0
                    AND m.Frequency > 0
                    """.format(self.metal, self.metal)

        self.c.execute(query, (username,))

        results = self.c.fetchall()

        if results:
            return results
        else:
            self.NoResultsError()

# class to display gui and control graph plotting
class Analyse:
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls, username, screen):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(Analyse, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.

    def __init__(self, username, screen):
        # Initialize attributes
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        self.Username = username

        self.screen = screen
        pygame.display.set_caption('Analyse')

        # Set up GUI elements
        self.SetupGui()
        # Graph surface created
        self.GraphSurface = pygame.Surface((self.WIDTH * 0.4, self.HEIGHT * 0.65))
        self.GraphSurface.fill((0, 255, 255))
        self.font = pygame.font.Font(None, int(self.WIDTH * 38 / 1536))

    # Method to display a message indicating no data to display
    def EmptyGraph(self):
        self.GraphSurface.fill((0, 255, 255))
        text_surface = self.font.render("Select a Metal\n And Graph To\n    Display", True, "black", )
        self.GraphSurface.blit(text_surface, (self.WIDTH * 230 / 1536, self.HEIGHT * 250 / 864))

    # Method to set up GUI elements
    def SetupGui(self):
        # Create a UIManager to manage UI elements from the pygame_ui library
        self.ui_manager = pygame_gui.UIManager((int(self.WIDTH), int(self.HEIGHT)), "Resources/Styling/ButtonTheme.JSON")

        # Define the container rectangle for the scrollable container
        container_Rect = pygame.Rect(self.WIDTH * 0.033, self.HEIGHT * 0.15, self.WIDTH * 0.2, self.HEIGHT * 0.579)
        self.scrollable_container = pygame_gui.elements.UIScrollingContainer(container_Rect, self.ui_manager)

        # Load and scale images for background, and buttons
        self.background_image = pygame.image.load('Resources/view data/MenuBackground.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        self.MetalsRect_image = pygame.image.load('Resources/analyse/MetalsRect.png').convert_alpha()
        self.MetalsRect_image = pygame.transform.scale(self.MetalsRect_image,
                                                       (self.WIDTH * 0.2064, self.HEIGHT * 0.764))

        self.MetalsTitle_image = pygame.image.load('Resources/analyse/metalstitle.png').convert_alpha()
        self.MetalsTitle_image = pygame.transform.scale(self.MetalsTitle_image,
                                                        (self.WIDTH * 0.157, self.HEIGHT * 0.065))

        self.GraphButtonRect = pygame.image.load('Resources/analyse/GraphsButtonsRect.png').convert_alpha()
        self.GraphButtonRect = pygame.transform.scale(self.GraphButtonRect, (self.WIDTH * 0.284, self.HEIGHT * 0.228))

        self.AnalyseTitle_image = pygame.image.load('Resources/analyse/AnalyseTitle.png').convert_alpha()
        self.AnalyseTitle_image = pygame.transform.scale(self.AnalyseTitle_image,
                                                         (self.WIDTH * 0.157, self.HEIGHT * 0.08))

        self.GraphTitle_image = pygame.image.load('Resources/analyse/DrawGraphTitle.png').convert_alpha()
        self.GraphTitle_image = pygame.transform.scale(self.GraphTitle_image, (self.WIDTH * 0.2031, self.HEIGHT * 0.06))

        self.QuitButton_image = pygame.image.load('Resources/ButtonImages/QuitButton.png').convert_alpha()
        self.QuitButton = buttons.Button(0.02479, 0.84, 0.1758, 0.1146, self.QuitButton_image, self.WIDTH, self.HEIGHT)

        # Initialise lists to store metal buttons and graph buttons
        self.MetalButtons = []
        self.GraphButtons = []

        # Define the list of metals and create buttons for each metal
        metals = ['Aluminium', 'Beryllium', 'Caesium', 'Calcium', 'Cobalt', 'Gold', 'Iron', 'Lead', 'Mercury', 'Sodium',
                  'Uranium', 'Zinc']
        for count, metal in enumerate(metals): # iterate throuhg the list of buttons
            # dynamically create buttons and calculate their positions inside the scrollable rectangle
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0.228 * container_Rect.width,
                                          count * 0.2 * container_Rect.height,
                                          0.49 * container_Rect.width,
                                          0.14 * container_Rect.height),
                text=f'{metal}',
                manager=self.ui_manager,
                container=self.scrollable_container,
                object_id="#ViewData"
            )
            # add newly created button to list
            self.MetalButtons.append(button)

        # dimensions for graph buttons
        button_width = self.WIDTH * 0.117
        button_height = self.HEIGHT * 0.0579
        button_padding_x = self.WIDTH * 0.013
        button_padding_y = self.HEIGHT * 0.023

        # list containing text for graph buttons
        graphs = ["KE vs F", "I vs F", "I vs i", "KE vs i"]
        for count, graph in enumerate(graphs):
            # Dynamically create the buttons, calculating their positions on the screen
            # according to the window size and button size
            # Position buttons in a 2x2 style arrangement
            col = count % 2
            row = count // 2
            x = (self.WIDTH * 0.7135) + col * (button_width + button_padding_x)
            y = (self.HEIGHT * 0.8194) + row * (button_height + button_padding_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            button = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=f'{graph}',
                manager=self.ui_manager,
                object_id="#ViewData"
            )
            self.GraphButtons.append(button)
        # update size of scrollable container based on sizes of buttons
        scrollable_dimensions = (self.WIDTH * 0.1823, self.HEIGHT * 1.42)
        self.scrollable_container.set_scrollable_area_dimensions(scrollable_dimensions)

    # Method to draw the page
    def draw_page(self):
        clock = pygame.time.Clock()
        # Position of static gui elements
        MetalsRect_pos = ((self.WIDTH * 0.038), (self.HEIGHT * 0.056))
        MetalsTitle_pos = ((self.WIDTH * 0.06), (self.HEIGHT * 0.0637))
        GraphButtonsRect_pos = ((self.WIDTH * 0.7), (self.HEIGHT * 0.7371))
        AnalyseTitle_pos = ((self.WIDTH * 0.4212), (self.HEIGHT * 0.0231))
        GraphTitle_pos = ((self.WIDTH * 0.74), (self.HEIGHT * 0.748))
        GraphSurface_pos = ((self.WIDTH * 0.28), (self.HEIGHT * 0.12))

        # Stores metal selected to display graph for
        selected_metal = None
        # Sores type of graph chosen to display
        selected_graph = None

        Current_Graph = None
        self.EmptyGraph()
        drawn = False

        while True:
            time_delta = clock.tick(60) / 1000.0
            self.screen.fill((255, 255, 255))
            # display static gui elements on screen
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.MetalsRect_image, MetalsRect_pos)
            self.screen.blit(self.MetalsTitle_image, MetalsTitle_pos)
            self.screen.blit(self.GraphButtonRect, GraphButtonsRect_pos)
            self.screen.blit(self.AnalyseTitle_image, AnalyseTitle_pos)
            self.screen.blit(self.GraphTitle_image, GraphTitle_pos)

            quit = self.QuitButton.draw(self.screen)

            # quit button logic
            if quit:
                return 1

            #   ====== Graph Plotting =============

            # Plot the graph if both a metal and graph type are selected
            if selected_graph is not None and selected_metal is not None:
                # Determine which graph type was selected and create the corresponding graph object

                if selected_graph.text == "KE vs F":
                    Current_Graph = KE_VS_F(selected_metal.text, "KE_vs_F", self.Username)

                elif selected_graph.text == "I vs F":
                    Current_Graph = I_vs_F(selected_metal.text, "I_vs_F", self.Username)

                elif selected_graph.text == "I vs i":
                    Current_Graph = I_vs_i(selected_metal.text, "I_vs_i", self.Username)

                elif selected_graph.text == "KE vs i":
                    Current_Graph = KE_vs_i(selected_metal.text, "KE_vs_i", self.Username)

                # Retrieve data for the graph and calculate coordinates
                Current_Graph.results = Current_Graph.RetrieveData(None, None, None)
                drawable = Current_Graph.CalculateCoordinates()

                # If drawable, clear the graph surface, draw the graph, and enable the selected graph button
                if drawable:
                    Current_Graph.EmptyGraphAxis()
                    drawn = Current_Graph.DrawGraph()
                else:
                    # If not drawable, display a no results error
                    Current_Graph.NoResultsError()
                # Update the graph surface with the drawn graph or appropriate error

                if not drawn:
                    Current_Graph.NoResultsError()


                self.GraphSurface = Current_Graph.GetSurface()

                # Enable the selected graph button and reset selected_graph to None
                selected_graph.enable()
                selected_graph = None

            else:
                # If no graph is selected, display the current graph surface
                self.screen.blit(self.GraphSurface, GraphSurface_pos)

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    left_button_down = False

                # Check for button clicks
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element in self.MetalButtons:
                        # Disable all metal buttons except the one clicked and store the selected metal
                        for button in self.MetalButtons:
                            if button.check_pressed():
                                button.disable()
                                selected_metal = button
                            else:
                                button.enable()

                    elif event.ui_element in self.GraphButtons and selected_metal is not None:
                        # If a metal is already selected and a graph is selected
                        for button in self.GraphButtons:
                            if button.check_pressed():
                                # disable the selected graph button
                                button.disable()
                                # update selected graph variable
                                selected_graph = button
                            else:
                                # if the button was not selected, ensure it is enabled then continue
                                button.enable()

                # Process pygame_gui library widgets
                self.ui_manager.process_events(event)

            # update gui
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()
