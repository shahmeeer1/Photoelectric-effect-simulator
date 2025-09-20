
import sqlite3 
from .graphTemplate import graphTemplate


class Graph:

    #   Continued from custom initialiser
    def __init__(self, metalName, graph_dimensions):

        self.graphTemplate = None

        self.metal = metalName
        self.results = []
        self.coords = []
        self.cache = {}

        self.x_var = ""
        self.y_var = ""

        # Connect to database
        self.conn = sqlite3.connect('Simulator/SimData.db')
        self.c = self.conn.cursor()

    def CalculateCoordinates(self):
        pass

    def GetSurface(self):
        return self.graphTemplate.screen

    def LoadingGraph(self):
        graphTemplate.clear
        graphTemplate.display_message("Loadiing...")

    def NoResultsError(self):
        graphTemplate.clear
        graphTemplate.display_message("No results\n   Found")

    def RetrieveData(self):
        query = """ SELECT ?, ?
                    FROM results
                    WHERE MetalName = ?"""
        
        self.c.execute(query, (self.x_var, self.y_var, self.metal,))
        return self.c.fetchall()

