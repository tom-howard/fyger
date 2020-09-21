"""An open loop controller to make a robot follow a square motion path."""

from controller import Robot
from math import pi # from the python "math" module import the "pi" variable

# Create an instance of the robot:
robot = Robot()
# get the time step of the simulation (See WorldInfo > basicTimeStep 
# in the scene tree):
timestep = int(robot.getBasicTimeStep()) # in milliseconds

# Create an object for each of the robots wheels:
leftWheel = robot.getMotor('left wheel motor')
rightWheel = robot.getMotor('right wheel motor')
leftWheel.setPosition(float('inf'))
rightWheel.setPosition(float('inf'))
leftWheel.setVelocity(0.0)
rightWheel.setVelocity(0.0)

# some key robot geometries and equations of motion calculations:
wheel_diameter = 0.05 # meters
robot_diameter = 0.09 # meters (the distance between the two wheels)
# We can find out the maximum velocity of our robots wheels by
# accessing the .getMaxVelocity() function from either of our wheels
# (it is the same for both)
max_velocity = leftWheel.getMaxVelocity() # radians per second
# print this to the console so that we can see what it is:
print('The Robot max wheel velocity is {} rad/s'.format(max_velocity))
wheel_circumference = pi * wheel_diameter # meters

# calculate the time required to move 0.5 meters in a straight line:
fwd_displacement = 0.5 / wheel_circumference # wheel revolutions
# one wheel revolution is 2*pi radians, so:
fwd_displacement = 2 * pi * fwd_displacement # in radians
# time required to travel this far:
fwd_duration = fwd_displacement / max_velocity # in seconds
# find out how many simulation time steps this duration represents:
fwd_timeSteps = fwd_duration / (timestep / 1000) # time steps
# convert this to the nearest whole number and add a bit to account for any delays
fwd_timeSteps = int(fwd_timeSteps) + 2

# Now, calculate the time required to turn on the spot by 90 degrees:
wheel_linear_velocity = (wheel_diameter / 2) * max_velocity # meters per second
robot_angular_velocity = wheel_linear_velocity / (robot_diameter / 2) # rad/s
# 90 degrees is pi/2 radians, so time to turn through this displacement is:
turn_duration = (pi / 2) / robot_angular_velocity # seconds
# find the number of whole simulation time steps this relates to
# (again, plus a bit extra):
turn_timeSteps = int(turn_duration / (timestep / 1000)) + 3

# get the robot's Compass device and enable it:
compass = robot.getCompass("compass")
compass.enable(timestep)

# The main loop:
# Repeat the loop 4 times (once for each side of the square):
while robot.step(timestep) != -1:
    leftWheel.setVelocity(3)
    rightWheel.setVelocity(-3)

print('No more loops, stopping the robot...')
# Set wheel velocityes to zero to over-ride position control and stop the robot:
leftWheel.setVelocity(0)
rightWheel.setVelocity(0)

print('Finished.')