import pygame
import math

class graphTemplate:
    def __init__(self, graph_dimensions, x_axis_at_zero=True, x_range=(0, 9), y_range=(0, 9), x_step=None, y_step=None):

        self.screen = pygame.Surface(graph_dimensions)   # Surface to draw the graph on
        #self.screen = pygame.display.set_mode((800, 600))   # Surface to draw the graph on
        self.font = pygame.font.SysFont(None, 24)       # Default font for labels

        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.running = True

        self.x_axis_at_zero = x_axis_at_zero    # If False, X axis is halfway up the Y axis
        self.x_range = x_range                  # (min, max) for X axis
        self.y_range = y_range                  # (min, max) for Y axis
        self.x_step = x_step                    # Step size for X axis ticks/labels
        self.y_step = y_step                    # Step size for Y axis ticks/labels

        self.y_axis_x = 70      # X position of Y axis
        self.x_axis_y = self.HEIGHT - 50 if x_axis_at_zero else self.HEIGHT // 2    # Y position of x axis


    """ Draws the X and Y axes and ticks on the graph surface. """
    def draw_graph(self):

        # Draw X and Y axes
        # Draw X axis
        pygame.draw.line(self.screen,   # surface
                         (0, 0, 0),     # colour
                         (self.y_axis_x, self.x_axis_y),    # start position
                         (self.WIDTH - 50, self.x_axis_y),  # end position
                         2)  # width
        
        # Draw Y axis
        pygame.draw.line(self.screen, (0, 0, 0), (self.y_axis_x, self.HEIGHT - 50), (self.y_axis_x, 50), 2)  # Y-axis


        self.draw_x_ticks()
        self.draw_y_ticks()


    """ Calculates position of and draws intervals/ticks on X axis"""

    def draw_x_ticks(self):
        # Draw ticks and labels on X-axis
        x_min, x_max = self.x_range
        x_step = self.x_step

        # Calculate step if not provided
        if x_step is None:
            x_step = (x_max - x_min) // 9 if x_max != x_min else 1
        
        # Calculate number of ticks
        num_x_ticks = int(round((x_max - x_min) / x_step)) + 1

        # Draw ticks
        for i in range(num_x_ticks):
            x_label_val = x_min + i * x_step    # calculate label value

            # Calculate pixel position
            x = self.y_axis_x + ((x_label_val - x_min) / (x_max - x_min)) * (self.WIDTH - self.y_axis_x - 50)
            #   Add left padding + scaled multiplier * available width

            # Draw tick
            pygame.draw.line(self.screen, (0, 0, 0), (x, self.x_axis_y), (x, self.x_axis_y + 5), 2)

            # Format label
            if abs(x_step) < 1:
                # Use 2 decimal places for small steps
                label = self.font.render(f"{x_label_val:.2f}", True, (0, 0, 0))
            else:
                label = self.font.render(f"{x_label_val:.0f}", True, (0, 0, 0))

            # Shift the first label a little to the right to avoid overlapping with Y axis
            if i == 0:
                self.screen.blit(label, (x - label.get_width() // 2 + 10, self.x_axis_y + 10))
            else:
                self.screen.blit(label, (x - label.get_width() // 2, self.x_axis_y + 10))


    """ Calculates position of and draws intervals/ticks on Y axis"""

    def draw_y_ticks(self):
        # Draw ticks and labels on Y-axis
        y_min, y_max = self.y_range
        y_step = self.y_step

        # Calculate step if not provided
        if y_step is None:
            y_step = (y_max - y_min) // 9 if y_max != y_min else 1
        
        # Calculate number of ticks
        num_y_ticks = int(round((y_max - y_min) / y_step)) + 1

        # Draw ticks
        for i in range(num_y_ticks):
            y_label_val = y_min + i * y_step   # calculate label value

            # Skip labels outside the defined range (with small tolerance for floating point errors)
            if y_label_val > y_max + 1e-8:
                continue

            # Calculate pixel position
            y = self.HEIGHT - 50 - ((y_label_val - y_min) / (y_max - y_min)) * (self.HEIGHT - 100)
            #   Start from bottom padding - scaled multiplier * available height

            # Draw tick
            pygame.draw.line(self.screen, (0, 0, 0), (self.y_axis_x - 5, y), (self.y_axis_x, y), 2)

            # Format label
            if abs(y_step) < 1:
                # Use 2 decimal places for small steps
                label = self.font.render(f"{y_label_val:.2f}", True, (0, 0, 0))
            else:
                label = self.font.render(f"{y_label_val:.0f}", True, (0, 0, 0))

            # Draw label to the left of the Y axis
            self.screen.blit(label, (self.y_axis_x - label.get_width() - 10, y - label.get_height() // 2))

    """ Plots a list of (x, y) points on the graph surface. """
    def plot_points(self, points):
        # Points is a list of (x, y) tuples
        y_min, y_max = self.y_range
        x_min, x_max = self.x_range

        for i in points:
            x_val, y_val = i

            y = self.HEIGHT - 50 - ((y_val - y_min) / (y_max - y_min)) * (self.HEIGHT - 100)
            x = x = self.y_axis_x + ((x_val - x_min) / (x_max - x_min)) * (self.WIDTH - self.y_axis_x - 50)
            pygame.draw.circle(self.screen, "black", (x, y), 4)


    def draw_x_label(self, label):
        text = self.font.render(label, True, (0, 0, 0))
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT - 30))

    def draw_y_label(self, label):
        text = self.font.render(label, True, (0, 0, 0))
        # Rotate the text surface for vertical display
        rotated_text = pygame.transform.rotate(text, 90)
        self.screen.blit(rotated_text, (20, self.HEIGHT // 2 - rotated_text.get_height() // 2))

    def clear(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with white

    def display_message(self, message):
        text = self.font.render(message, True, (0, 0, 0))
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2))

    def draw_page(self):
        clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        self.draw_graph()
        self.draw_x_label("X Axis")
        self.draw_y_label("Y Axis")
        self.plot_points([(1,1), (2,4), (3,9), (4,6), (5,2), (6,3)])

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # self.screen.fill((255, 255, 255))  # Fill the screen with white
            # self.draw_axes()
            # Add drawing code here
            pygame.display.flip()  # Update the full display Surface to the screen
            clock.tick(10)  # Limit to 60 frames per second

    def set_x_range(self, range, step):
        self.x_range = range
        self.x_step = step

    def set_y_range(self, range, step):
        self.y_range = range
        self.y_step = step
    

#pygame.init()
# # Example usage: set x axis from -5 to 5 with step 2, y axis from 0 to 100 with step 20
#temp = graphTemplate(x_axis_at_zero=False, x_range=(0, 10), y_range=(-10, 10), x_step=1, y_step=2)
#wiin = pygame.display.set_mode((800, 600))
# temp.draw_page()