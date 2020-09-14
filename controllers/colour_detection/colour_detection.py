"""colour_detection controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Initialise the motors and set target position to infinity (for speed control):
left_motor = robot.getMotor("left wheel motor")
right_motor = robot.getMotor("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
# set a speed variable:
SPEED = 4

# Initialise the camera:
camera = robot.getCamera("camera")
camera.enable(timestep)
width = camera.getWidth()
height = camera.getHeight()

pause_counter = 0
left_motor_speed = 0
right_motor_speed = 0
red = 0
green = 0
blue = 0
# Main loop:
# this runs until the simulation is stopped
while robot.step(timestep) != -1:
    if pause_counter > 0:
        pause_counter -= 1

    # Case 1:
    # A colour blob was found recently
    # The robot waits in front of it until pause_counter is decremented enough:
    if pause_counter > 10:
        left_motor_speed = 0
        right_motor_speed = 0
    # Case 2:
    # A colour blob was found more recently
    # The robot begins to turn but shouldn't analyse any camera images just now,
    # otherwise the same colour blob would be found again:
    elif pause_counter > 0:
        left_motor_speed = -SPEED
        right_motor_speed = +SPEED
    # Case 3:
    # The robot turns and analyses the camera image in order to find a new colour blob
    else:
        red = 0
        green = 0
        blue = 0

        image = camera.getImageArray()
        for x in range(int(width/3),int(2*width/3)):
            for y in range(int(height/2), int(3*height/4)):
                red = red + image[x][y][0]
                green = green + image[x][y][1]
                blue = blue + image[x][y][2]

        if (red > (3 * green)) and (red > (3 * blue)):
            current_blob = "red"
        elif (green > (3 * red)) and (green > (3 * blue)):
            current_blob = "green"
        elif (blue > (3 * red)) and (blue > (3 * green)):
            current_blob = "blue"
        else:
            current_blob = "none"

        # Case 3a:
        # No colour is detected, so the robot continues to turn:
        if current_blob == 'none':
            left_motor_speed = -SPEED
            right_motor_speed = SPEED

        # Case 3b:
        # A colour has been detected, so the robot stops and reports this:
        else:
            left_motor_speed = 0.0
            right_motor_speed = 0.0
            print("A {} coloured object has been detected.".format(current_blob))
            pause_counter = 20

    # set the motor speeds:
    left_motor.setVelocity(left_motor_speed)
    right_motor.setVelocity(right_motor_speed)