import re

class GUIValidation:
    
    def __init__(self, guimanager, initial_wavelength):
        self.gui = guimanager
        self.initial_wavelength = initial_wavelength

    def wavelength_validation(self, currentValue, inputted_value):
        # method to validate wavelength value input using regular expressions
        """
            ([0-9]{,3}): Matches any digits between 0-9 that ois 0-3 digits long
            ([.]([0-9]{1,2}))? : Matches any 1 or 2 digits between 0-9 that are
                                 preceded by a decimal point. The ? signifies that
                                 there must be 0 or 1 of the group preceding it meaning
                                 the input may be integer of float with 1 or 2 digits
                                 after the decimal.
            Examples of valid inputs according to this expression: 123, 1.23, 456.7
        """
        try:
            if re.fullmatch("([0-9]{0,3})([.]([0-9]{1,2}))?", inputted_value):
                if 300.00 <= float(inputted_value) <= 750.00: # only allow inputs between 300 and 750
                    return True
            else:
                return False
        except:
            self.return_to_valid_state(currentValue)
            # resets the input box after invalid input and displays error


    def return_to_valid_state(self, currentValue):
        try:
            # set wavelength slider to the current value for wavelength
            self.gui.set_text(str(currentValue))
            self.gui.set_current_value(float(currentValue))

        except:
            # In the case of an error, the frequency slider is reset to its
            # initial state using the initial state attributes
            self.gui.set_text(str(self.Initial_wavelength))
            self.gui.set_current_value(self.Initial_wavelength)
    
    def update_spectrum_slider(self, currentValue, inputted_value):
        # The wavelength output box and slider are updated using this method whenever a change takes place.
        try:
            self.gui.set_current_value(float(inputted_value))
            self.gui.set_text(str(float(inputted_value)))
            self.gui.rebuild()
        except:
            # In the case of an error, the error window is displayed and the entry value is reset to the previous value
            #self.error_window()
            self.gui.set_text(str(currentValue))