import joystick
import drivetrain
import time

joystick = joystick.Joystick()
if not joystick.isInitialized:
    print("Joystick failed initialization:", joystick.initializationError)
    exit

driveTrain = drivetrain.DriveTrain()
driveTrain.setSpeedDivisor(4)

print("Press and hold button 11 to stop.")

# Note that button 10 is labeled 11 on the joystick.
while not joystick.isButtonPressed(10):
    x, y, z = joystick.getAxes()
    #print(x, y, z)
    driveTrain.driveHybrid(x, y, z)
    time.sleep(0.020)

print("STOPPED!")
driveTrain.stop()
