from .graph_base import Graph
from .graphTemplate import graphTemplate


class KE_VS_F(Graph):
    def __init__(self, metal, graph_dimensions):
        super().__init__(metal,graph_dimensions)
        self.graph_dim = graph_dimensions
        self.x_var = "Frequency"
        self.y_var = "KineticEnergy"

        self.min_x = self.min_y = self.max_x = self.max_y = 0


    # Method to draw empty graph axes
    def EmptyGraphAxis(self):
        
        self.graphTemplate = graphTemplate(self.graph_dim, False, 
                                           (self.min_x, self.max_x), (self.min_y, self.max_y))
        self.graphTemplate.clear()
        self.graphTemplate.draw_graph()
        self.graphTemplate.draw_x_label(self.x_var)
        self.graphTemplate.draw_y_label(self.y_var)

    def DrawGraph(self):
        self.processResults()
        self.EmptyGraphAxis()
        self.graphTemplate.plot_points(self.results)

        # Line = Regression(self.coords)
        # drawn = Line.draw_line(self.GraphSurface, self.x.topleft[0], self.x.topright[0], True, self.y.bottomright[1])
        # return drawn

    # Method to retrieve data from database
    def processResults(self):
        self.results = super().RetrieveData()
        self.results = [(a, b * 100) for (a,b) in self.results] # only keep results > 0 after rounding
        print("\nUpdated results: {}".format(self.results))

        self.min_x = min(row[0] for row in self.results) - 100
        self.min_y = max(row[1] for row in self.results) * -1 #min(row[1] for row in self.results)

        self.max_x = max(row[0] for row in self.results)
        self.max_y = max(row[1] for row in self.results)



            