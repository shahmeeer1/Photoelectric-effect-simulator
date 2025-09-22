import pygame
"""
pygame used for gui


Overriding of __new__ method used from Stackoverflow.
Lines: 32 - 35
https://stackoverflow.com/a/1810367

"""
#   Initialise pygame
pygame.init()


#   Abstract base class for defining states
class State:
    _instance = None

    #   Singleton pattern ensures that only one object per class can exist at a time
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
        return cls._instance

    #   Runs instructions for the current state
    def Current(self):
        raise NotImplementedError

    #   Determines transition to next state
    def Transition(self, input):
        raise NotImplementedError




""" State for initialising the GUI. This is necessary
    to ensure that the same window is used for all pygame states."""


class GuiInitialise(State):
    #   screen / window is stored in class method
    __screen = None

    @classmethod
    def GetScreen(cls):
        return cls.__screen

    def Current(self):
        #   Retrieves monitor resolution
        info = pygame.display.Info()
        #   Creates window that fills 80% of the screen
        WIDTH, HEIGHT = info.current_w * 0.8, info.current_h * 0.8
        GuiInitialise.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        return 1

    #   Returns Menu state regardless of input
    def Transition(self, input):
        return MenuState()


#   State representing main menu
class MenuState(State):

    #   Launches menu screen gui
    def Current(self):
        import MenuGui
        Menu = MenuGui.Menu(GuiInitialise.GetScreen()).draw_menu()
        return Menu

    #   Transitions to different states based on menu selection
    def Transition(self, input):
        match input:
            case 1:
                return SelectMetalsState()
            case 2:
                return ViewDataState()
            case 3:
                return AnalyseState()
            case 4:
                return TheoryState()
            case _:
                raise ValueError(f"Invalid input: {input}")


"""Update to utilise model instead of passing data between states"""
#   State for selecting metals
class SelectMetalsState(State):
    #   Class variable grants global access to selected metals
    __SelectedMetals = []

    #   Class method to retrieve selected metals list
    @classmethod
    def GetSelectedMetals(cls):
        return cls.__SelectedMetals

    #   Launches select metals screen
    def Current(self):
        #TODO: SHOULD NOT INJECT DATA INTO STATE
        import SelectMetals
        page = SelectMetals.SelectMetals(GuiInitialise.GetScreen())
        option, SelectMetalsState.__SelectedMetals = page.draw_page()
        return option

    #   Transitions to simulation or back to menu
    def Transition(self, input):
        if input == 1:
            return SimulatorState()
        elif input == 2:
            return MenuState()


#   State for running simulator
class SimulatorState(State):
    def Current(self):
        import sim.Simulator as Simulator
        #   Screen and list of selected metals passed as arguments
        Sim = Simulator.Simulation(SelectMetalsState.GetSelectedMetals(), GuiInitialise.GetScreen())
        option = Sim.draw_sim()
        return option

    #   Transitions to Save Results state or back to select metals screen
    def Transition(self, input):
        if input == 1:
            return SaveResultsState()  # Return to Menu or return to select metals page
        elif input == 2:
            return SelectMetalsState()

    """
    Need to update to remove credentials
    """
#   State for saving simulation results to database
class SaveResultsState(State):
    def Current(self):
        #TODO: SHOULD NOT INJECT DATA INTO STATE
        import SaveResults
        #   selected metals list 
        save = SaveResults.SaveData(SelectMetalsState.GetSelectedMetals())
        return save

    #   Returns to menu screen
    def Transition(self, input):
        if input == 1:
            return MenuState()

"""Requires credentials"""
# State for viewing data
class ViewDataState(State):
    def Current(self):
        #TODO: SHOULD NOT INJECT DATA INTO STATE
        import ViewData

        view = ViewData.ViewData(GuiInitialise.GetScreen())
        option = view.draw_page()
        return option

    #   Transitions back to main menu
    def Transition(self, input):
        if input == 1:
            return MenuState()


# State for analyzing data
class AnalyseState(State):
    #TODO: SHOULD NOT INJECT DATA INTO STATE
    def Current(self):
        import analysee.analyse_gui as analyse_gui

        analysis = analyse_gui(GuiInitialise.GetScreen())
        option = analysis.draw_page()
        return option

    #   Returns back to main menu
    def Transition(self, input):
        if input == 1:
            return MenuState()

class TheoryState(State):

    def Current(self):
        import Theory
        t = Theory.Theory(GuiInitialise.GetScreen())
        option = t.draw_page()
        return option

    def Transition(self, input):
        if input == 1:
            return MenuState()



""" 
    State for initialising programme. Responsible for creating 
    database if it does not already exist; ensuring that
    all tables are correctly populated and correcting any 
    errors in the tables.
"""
class Initialise(State):
    def Current(self):
        import DatabaseSetup
        dbsetup = DatabaseSetup.database_setup().Database_Status()
        return dbsetup

    def Transition(self, input):
        if input == 1:
            return GuiInitialise()
        else:
            print("Error initialising programme")
            return False
        #   when a function returns False, this indicates an error.


#   Class representing the State machine and state transition mechanism.
class StateMachine:
    def __init__(self):
        self.CurrentState = Initialise()

    #   Executes the main loop of the programme and handles state transitions
    def run_state(self):

        """
            Checks if a current state is active and the boolean False has not been returned
            from the previous 'next' method.
            False indicates an error with initialising the programme
        """

        while self.CurrentState is not None:
            if self.CurrentState:
                transition = self.CurrentState.Current()
                self.CurrentState = self.CurrentState.Transition(transition)


            elif not self.CurrentState:
                #   programme will terminate here due to incorrectly setup database
                pass

#   Runs the state machine

if __name__ == "__main__":
    sim = StateMachine()
    sim.run_state()
