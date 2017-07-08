import RPi.GPIO as GPIO

# The following define indices for the two motors:
_LEFT = 0
_RIGHT = 1

# The following define the GPIO pins used to control the two motors.
# Note that we use the BCM pin numbering scheme.

# For each motor there are three pins:
#   The first and second pins set motor direction
#   The third pin controls the PWM signal
_MOTOR_PINS = [ [20, 21, 26], [6, 13, 12] ]

# Motor direction is set via two pins for each motor:
# Pin1  Pin2  Direction
# ====  ====  =========
#    0     0  Stopped
#    0     1  Reverse
#    1     0  Forward
#    1     1  Stopped

# The PWM frequency:
_FREQ = 500

class DriveTrain:
    """Controls a simple drive train."""
    
    def __init__(self):
        
        # Configure GPIO pins:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for m in range(_LEFT, _RIGHT + 1):
            for p in range(0, 3):
                GPIO.setup(_MOTOR_PINS[m][p], GPIO.OUT)

        # The following creates an array of two PWM channels, one for each motor:
        self._pwms = [ GPIO.PWM(_MOTOR_PINS[_LEFT][2], _FREQ), GPIO.PWM(_MOTOR_PINS[_RIGHT][2], _FREQ) ]

        # Set the default speed divisors:
        self._longitudinalSpeedDivisor = 1
        self._turnSpeedDivisor = 1
        
        # Make sure everything is stopped:
        self._stop(_LEFT)
        self._stop(_RIGHT)
        self._pwms[_LEFT].start(0)
        self._pwms[_RIGHT].start(0)
        
    # Tells the specified motor to move in forward direction:
    def _forward(self, motor):
        GPIO.output(_MOTOR_PINS[motor][0], 1)
        GPIO.output(_MOTOR_PINS[motor][1], 0)

    # Tells the specified motor to move in reverse direction:
    def _reverse(self, motor):
        GPIO.output(_MOTOR_PINS[motor][0], 0)
        GPIO.output(_MOTOR_PINS[motor][1], 1)

    # Tells the specified motor to stop:
    def _stop(self, motor):
        GPIO.output(_MOTOR_PINS[motor][0], 0)
        GPIO.output(_MOTOR_PINS[motor][1], 0)

    # Tells the specified motor to turn a specified speed between -100 and 100:
    def _setSpeed(self, motor, speedVal):
        # Set appropriate direction:
        if speedVal < 0:
            self._reverse(motor)
        else:
            self._forward(motor)

        # Set speed:
        self._pwms[motor].ChangeDutyCycle(abs(speedVal))

    # Sets the divisor to limit max turn speed.
    def setTurnSpeedDivisor(self, speedDivisor):
        self._turnSpeedDivisor = speedDivisor
 
    # Sets the divisor to limit maxlongitudinal (forward/backward) speed.
    def setLongitudinalSpeedDivisor(self, speedDivisor):
        self._longitudinalSpeedDivisor = speedDivisor       

    # Drives using a hybrid method using the axis values from a joystick.
    # All axis values are between -1.0 and +1.0.
    # In this method:
    #     The y axis value controls forward/backward motion
    #     The z axis (twist) controls turning in place
    def driveHybrid(self, x, y, z):
        # Determine which axis is dominant:
        if abs(z) > abs(y):
            # Turn left for negative z and turn right for positive z
            self._setSpeed(_LEFT, z * 100 / self._turnSpeedDivisor)
            self._setSpeed(_RIGHT, -z * 100 / self._turnSpeedDivisor)
        else:
            # Move forward or backward (note that negative y values indicate forward movement):
            self._setSpeed(_LEFT, -y * 100 / self._longitudinalSpeedDivisor)
            self._setSpeed(_RIGHT, -y * 100 / self._longitudinalSpeedDivisor)

    # Stops all motors.
    def stop(self):
        self._stop(_LEFT)
        self._stop(_RIGHT)
        
    


