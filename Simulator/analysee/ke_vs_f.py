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
        
        self.graphTemplate = graphTemplate(self.graph_dim, True, 
                                           (self.min_x, self.max_x), (self.min_y, self.max_y))
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
        self.results = [i for i in self.results if round(i[0], 2) > 0.00] # only keep results > 0 after rounding

        self.min_x = min(row[0] for row in self.results)
        self.min_y = min(row[1] for row in self.results)

        self.max_x = max(row[0] for row in self.results)
        self.max_y = max(row[1] for row in self.results)



            