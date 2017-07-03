import RPi.GPIO as GPIO




class DriveTrain:
    """Controls a simple drive train."""
    
    def __init__(self):
        # The following define indices for the two motors:
        self._LEFT = 0
        self._RIGHT = 1

        # The following define the GPIO pins used to control the two motors.
        # Note that we use the BCM pin numbering scheme.

        # For each motor there are three pins:
        #   The first and second pins set motor direction
        #   The third pin controls the PWM signal
        self._MOTOR_PINS = [ [20, 21, 26], [6, 13, 12] ]

        # Motor direction is set via two pins for each motor:
        # Pin1  Pin2  Direction
        # ====  ====  =========
        #    0     0  Stopped
        #    0     1  Reverse
        #    1     0  Forward
        #    1     1  Stopped

        # The PWM frequency:
        self._FREQ = 500
        
        # Configure GPIO pins:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for m in range(LEFT, RIGHT + 1):
            for p in range(0, 3):
                GPIO.setup(MOTOR_PINS[m][p], GPIO.OUT)

        # The following creates an array of two PWM channels, one for each motor:
        self._pwms = [ GPIO.PWM(self._MOTOR_PINS[self._LEFT][2], self._FREQ), GPIO.PWM(self._MOTOR_PINS[self._RIGHT][2], self._FREQ) ]

        # Set the default speed divisor:
        self._speedDivisor = 2
        
        # Make sure everything is stopped:
        self._stop(self._LEFT)
        self._stop(self._RIGHT)
        self._pwms[self._LEFT].start(0)
        self._pwms[self._RIGHT].start(0)
        
    # Tells the specified motor to move in forward direction:
    def _forward(self, motor):
        GPIO.output(self._MOTOR_PINS[motor][0], 1)
        GPIO.output(self._MOTOR_PINS[motor][1], 0)

    # Tells the specified motor to move in reverse direction:
    def _reverse(self, motor):
        GPIO.output(self._MOTOR_PINS[motor][0], 0)
        GPIO.output(self._MOTOR_PINS[motor][1], 1)

    # Tells the specified motor to stop:
    def _stop(self, motor):
        GPIO.output(self._MOTOR_PINS[motor][0], 0)
        GPIO.output(self._MOTOR_PINS[motor][1], 0)

    # Tells the specified motor to turn a specified speed between -100 and 100:
    def _speed(self, motor, speedVal):
        # Set appropriate direction:
        if speedVal < 0:
            reverse(motor)
        else:
            forward(motor)

        # Set speed:
        self._pwms[motor].ChangeDutyCycle(abs(speedVal))

    def setSpeedDivisor(self, speedDivisor):
        self._speedDivisor = speedDivisor

    # Drives using a hybrid method using the axis values from a joystick.
    # All axis values are between -1.0 and +1.0.
    # In this method:
    #     The y axis value controls forward/backward motion
    #     The z axis (twist) controls turning in place
    def driveHybrid(self, x, y, z):
        # Determine which axis is dominant:
        if abs(z) > abs(y):
            # Turn left for positive z and turn right for negative z
            self._speed(self._LEFT, -z * 100 / self._speedDivisor)
            self._speed(self._RIGHT, z * 100 / self._speedDivisor)
        else:
            # Move forward or backward (note that negative y values indicate forward movement):
            self._speed(self._LEFT, -y * 100 / self._speedDivisor)
            self._speed(self._RIGHT, -y * 100 / self.speedDivisor)
    


