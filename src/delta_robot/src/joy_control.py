#!/usr/bin/env python3


'''
	Matic Vodopivec
	13.6.2022

	Help:
	Moving delta robot with Logitech F710 gamepad.

'''


from re import I, S
import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from sensor_msgs.msg import Joy
import time

import numpy as np
import matplotlib.pyplot as plt 
import cv2

from supportingFunctions.minJerkInterpolator import minJerkInterpolator

class joystick_control:
	def __init__(self, boundries, displayResult=False):
		self.boundries = boundries

		# Read max velocity
		self.maxVel = rospy.get_param('/robot_max_vel')
		self.rotVel = rospy.get_param('/robot_rot_vel')
		
		self.start_time = time.time()
		self.time_flag = False
		self.dt = 0.001
		self.gripper_btn_old = 0
		self.close_gripper = False

		self.gripperClosedPosition = 0
		self.gripperOpenedPosition = -120

		# Set start position of the robot
		self.points_X = 0
		self.points_Y = 0
		self.points_Z = -650
		self.point_rot_z = 0

		self.joy = Joy()
		self.joy.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		self.joy.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		# User settings:
		nodeName = 'joy_control'
		self.topicName = '/r_control'
		nodeRate = 1000	# in Hz
		dT_ms = int(1000/nodeRate)

		rospy.init_node(nodeName)
		rate = rospy.Rate(5)

		# initialize Interpolator:
		maxSpeed = np.array([500, 500, 500, 200, 100])
		self.interpolator = minJerkInterpolator(maxSpeed=maxSpeed, dT=dT_ms*0.001, printAll=False)

		rospy.Subscriber("joy", Joy, self.callback_joy)

		self.pub = rospy.Publisher(self.topicName, numpy_msg(Floats),queue_size=1)

	def callback_joy(self, data):
		self.joy = data
		#print(self.joy)
		#self.generate_points()

	def generate_points(self):
		# Determine velocities in all directions

		# Check if deadman switch is pressed on gamepad
		deadman_switch = self.joy.buttons[5]
		print(deadman_switch)
		if deadman_switch:
			# X axis 
			vel_X = self.joy.axes[0] * self.maxVel
			#print(vel_X)
			# Y axis
			vel_Y = self.joy.axes[1] * self.maxVel
			# Z axis
			vel_Z = self.joy.axes[7] * self.maxVel
			# Rotation around Z axis
			rot_Z = self.joy.axes[6] * self.rotVel
			# Open/close gripper
			gripper_btn = self.joy.buttons[4]
		else:
			vel_X = 0
			vel_Y = 0
			vel_Z = 0
			rot_Z = 0
			gripper_btn = 0

		# opening and closing gripper
		if gripper_btn==1 and self.gripper_btn_old==0:
			self.close_gripper = not(self.close_gripper)
		self.gripper_btn_old = gripper_btn

		if self.close_gripper:
			gripper_poz = self.gripperClosedPosition
		else:
			gripper_poz = self.gripperOpenedPosition

		# Generate points
		self.points_X = self.points_X + vel_X * self.dt
		self.points_Y = self.points_Y + vel_Y * self.dt
		self.points_Z = self.points_Z + vel_Z * self.dt
		self.point_rot_z = self.point_rot_z + rot_Z * self.dt

		# Set limits in x direction
		if self.points_X < self.boundries[0][0]:
			# Negative limit
			self.points_X = self.boundries[0][0]
		elif self.points_X > self.boundries[0][1]:
			# Positive limit
			self.points_X = self.boundries[0][1]

		# Set limits in y direction
		if self.points_Y < self.boundries[1][0]:
			# Negative limit
			self.points_Y = self.boundries[1][0]
		elif self.points_Y > self.boundries[1][1]:
			# Positive limit
			self.points_Y = self.boundries[1][1]

		# Set limits in z direction
		if self.points_Z < self.boundries[2][0]:
			# Negative limit
			self.points_Z = self.boundries[2][0]
		elif self.points_Z > self.boundries[2][1]:
			# Positive limit
			self.points_Z = self.boundries[2][1]

		# Set limits in rotation around z axis
		if self.point_rot_z < self.boundries[3][0]:
			# Negative limit
			self.point_rot_z = self.boundries[3][0]
		elif self.point_rot_z > self.boundries[3][1]:
			# Positive limit
			self.point_rot_z = self.boundries[3][1]

		# Generate next point in trajectory
		next_point = np.array([self.points_X, self.points_Y, self.points_Z, self.point_rot_z, gripper_poz])

		self.interpolator.addPoint(next_point)     

		status, r_control = self.interpolator.run()

		if status > 0:
			
			r_control = r_control.astype(dtype=np.float32)
			print(r_control)
			self.pub.publish(r_control)

			x = r_control[0]
			y = r_control[1]   

		# Measuring cycle time
		self.dt = time.time() - self.start_time
		# Save current time
		self.start_time = time.time()
		
		self.pub = rospy.Publisher(self.topicName, numpy_msg(Floats),queue_size=1)
		#rate = rospy.Rate(5)
		#rospy.spin()

		print(self.dt)




if __name__ == '__main__':
	rospy.set_param('/robot_max_vel', 100)
	rospy.set_param('/robot_rot_vel', 80)

	# Call class
	# Set limits in x, y, z direction and also rotation around z axis
	boundries = [[-300, 300], [-300, 300], [-850, -500], [-180, 180] ]
	joy_control = joystick_control(boundries=boundries)
	rate = rospy.Rate(100)

	while not rospy.is_shutdown():
		joy_control.generate_points()
		rate.sleep()


	
