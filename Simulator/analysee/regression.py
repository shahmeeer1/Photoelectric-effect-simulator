import pygame

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