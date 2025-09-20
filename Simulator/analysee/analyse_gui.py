import pygame
import pygame_gui
import sqlite3
import buttons
import analysee.graphTemplate as gt
from .ke_vs_f import KE_VS_F
from .i_vs_f import I_VS_F
from .ke_vs_i import KE_VS_i
from .I_vs_i import I_VS_i

"""
pygame and pygame_ui library used for gui
sqlite3 used for database management

# buttons is my own file


some of the Overriding of __new__ method used from Stackoverflow.
https://stackoverflow.com/a/1810367
Lines: 716 - 710
"""
pygame.init()

# class to display gui and control graph plotting
class analyse_gui:
    _instance = None  # Check if an instance of this class already exists

    def __new__(cls, screen):  # method used to ensure only one object is created
        if cls._instance is None:  # If an instance does not exist, a new one will be created
            cls._instance = super(analyse_gui, cls).__new__(cls)
        return cls._instance  # If an instance already exists, it will be returned and used.

    def __init__(self, screen):
        # Initialize attributes
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        self.screen = screen
        pygame.display.set_caption('Analyse')

        # Set up GUI elements
        self.SetupGui()
        # Graph surface created
        self.GraphSurface = pygame.Surface((self.WIDTH * 0.4, self.HEIGHT * 0.65))
        self.GraphSurface.fill((0, 255, 255))
        self.font = pygame.font.Font(None, int(self.WIDTH * 38 / 1536))

        self.GraphDimensions = (self.WIDTH * 0.4, self.HEIGHT * 0.65)

    # Method to display a message indicating no data to display
    def EmptyGraph(self):
        holder = gt.graphTemplate((self.WIDTH * 0.4, self.HEIGHT * 0.65))
        holder.clear()
        holder.draw_graph()
        # self.GraphSurface.display_message("Select a Metal\n And Graph To\n    Display")
        self.GraphSurface = holder.screen

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
        # Stores type of graph chosen to display
        selected_graph = None

        Current_Graph = None
        #self.EmptyGraph()
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
                    Current_Graph = KE_VS_F(selected_metal.text, self.GraphDimensions)

                elif selected_graph.text == "I vs F":
                    Current_Graph = I_VS_F(selected_metal.text, self.GraphDimensions)

                elif selected_graph.text == "I vs i":
                    Current_Graph = I_VS_i(selected_metal.text, self.GraphDimensions)

                elif selected_graph.text == "KE vs i":
                    Current_Graph = KE_VS_i(selected_metal.text, self.GraphDimensions)

                # # Retrieve data for the graph and calculate coordinates
                # Current_Graph.results = Current_Graph.RetrieveData(None, None, None)
                # drawable = Current_Graph.CalculateCoordinates()

                # If drawable, clear the graph surface, draw the graph, and enable the selected graph button
                # if drawable:
                #     Current_Graph.EmptyGraphAxis()
                #     drawn = Current_Graph.DrawGraph()
                # else:
                #     # If not drawable, display a no results error
                #     Current_Graph.NoResultsError()
                # # Update the graph surface with the drawn graph or appropriate error

                # if not drawn:
                #     Current_Graph.NoResultsError()
                Current_Graph.DrawGraph()

                self.GraphSurface = Current_Graph.GetSurface()
                print("Surface retireved")

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
