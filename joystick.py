import pygame

class Joystick:
    """Class for getting data from the Joystick"""
    
    def __init__(self):
        # Axis indices:
        self._X = 0
        self._Y = 1
        self._Z = 2
        self._TRIM = 3

        # Initialization information:
        self.isInitialized = False

        # Initialize the whole pygame system:
        pygame.init()

        # Make sure we have at least one joystick:
        count = pygame.joystick.get_count()
        if count < 1:
            self.initializationError = "Joystick not found"
            return

        # Create the joystick object:
        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

        # Check for the expected number of axes:
        if self._joystick.get_numaxes() != 4:
            self.initializationError = "Expected 4 joystick axes, got {0}".format(self._joystick.get_numaxes())
            return

        self._joystick.init()
        self.isInitialized = True

    # Returns the values of the X, Y and Z axes:
    def getAxes(self):
        pygame.event.get()
        return self._joystick.get_axis(self._X), self._joystick.get_axis(self._Y), self._joystick.get_axis(self._Z)
    
    # Returns True if the specified button is pressed
    def isButtonPressed(self, button):
        return self._joystick.get_button(button)
        
