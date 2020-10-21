"""Demonstrationg the use of the compass."""

from controller import Robot

# create the Robot instance:
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

# Initialise the compass:
compass = robot.getCompass("compass")
compass.enable(timestep)

pause_counter = 0
left_motor_speed = 0
right_motor_speed = 0

# Main loop:
while robot.step(timestep) != -1:
    if pause_counter > 0:
        pause_counter -= 1
    
    if pause_counter > 10:
        left_motor_speed = 0
        right_motor_speed = 0
    elif pause_counter > 0:
        left_motor_speed = -SPEED
        right_motor_speed = +SPEED
    else:
        compass_values = compass.getValues()
        compass_x_value = compass_values[0]
        print(compass_x_value)
        if compass_x_value < -0.99:
            orientation = "SOUTH"
        elif compass_x_value > 0.99:
            orientation = "NORTH"
        else:
            orientation = "not north or south"
        
        if orientation == "not north or south":
            left_motor_speed = -SPEED
            right_motor_speed = +SPEED
        else:
            left_motor_speed = 0.0
            right_motor_speed = 0.0
            print("robot is pointing {} (the compass x value is {:.3f})".format(orientation, compass_x_value))
            pause_counter = 60
    
    # set the motor speeds:
    left_motor.setVelocity(left_motor_speed)
    right_motor.setVelocity(right_motor_speed)
    
    