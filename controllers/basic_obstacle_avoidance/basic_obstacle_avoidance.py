"""basic_obstacle_avoidance controller."""

from controller import Robot
import math

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

motors = []
encoders = []
for i, motor_name in enumerate(["left", "right"]):
    motor = robot.getMotor('{} wheel motor'.format(motor_name))
    enc = robot.getPositionSensor('{} wheel encoder'.format(motor_name))
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)
    enc.enable(timestep)
    motors.append(motor)
    encoders.append(enc)

# distance sensors:
distance_sensors = []
for i in range(2):
    sensor = robot.getDistanceSensor("ds{:}".format(i))
    sensor.enable(timestep)
    distance_sensors.append(sensor)

camera = robot.getCamera("camera")
camera.enable(timestep)

max_vel = motors[1].getMaxVelocity()
print("Max velocity is {:.3f} rad/s".format(max_vel))

speed_vectors = [1, -1]
ds_to_vel = 0.004

speed_offset = 0.3 * max_vel

# Main loop:
while robot.step(timestep) != -1:

    
    speed_delta = ds_to_vel * distance_sensors[0].getValue() - ds_to_vel * distance_sensors[1].getValue()
    
    encvals = []
    for i, motor in enumerate(motors):
        velocity = speed_offset + (speed_vectors[i] * speed_delta)
        motor.setVelocity(velocity)
        encvals.append(encoders[i].getValue() % (2 * math.pi))
    dist_vals = []
    for i, dist in enumerate(distance_sensors):
        dist_vals.append(dist.getValue())
    print("left = {:.0f}, right = {:.0f}.".format(dist_vals[0], dist_vals[1]))

