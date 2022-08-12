#!/usr/bin/env python3


'''
	Matic Vodopivec
	13.6.2022

	Help:
	Moving tracks with Logitech F710 gamepad.

'''


from re import I, S
import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from sensor_msgs.msg import Joy
from geometry_msgs.msg import TwistStamped
import time

import numpy as np
import matplotlib.pyplot as plt 
import cv2


class joystick_control:
	def __init__(self, displayResult=False):

		# Read max velocity
		self.maxVel    = rospy.get_param('/tracks_max_vel')
		self.maxRotVel = rospy.get_param('/tracks_max_rot_vel')
		
		self.start_time = time.time()
		self.dt = 0.001
		
		self.total_time = 0

		self.joy = Joy()
		self.joy.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		self.joy.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		self.setVel = self.maxVel / 2
		self.rotVel = self.maxRotVel / 3
		
		self.start_movement_btn_old = 0
		self.linear_movement = False

		# Define twist
		self.twist = TwistStamped()

		# User settings:
		nodeName = 'track_joy_control'
		self.topicName = '/tracks/twist_cmd'

		rospy.init_node(nodeName)

		rospy.Subscriber("joy", Joy, self.callback_joy)

		self.pub = rospy.Publisher(self.topicName, TwistStamped,queue_size=1)

	def callback_joy(self, data):
		self.joy = data

	def generate_points(self):
		# Determine velocities in all directions
		# Decrease and increase linear velocity (Y and A button on joystick)
		if self.joy.buttons[0]:
			self.setVel = self.setVel -  0.05* self.dt
			if self.setVel < 0:
				self.setVel = 0
		elif self.joy.buttons[3]:
			self.setVel = self.setVel + 0.05* self.dt
			if self.setVel > self.maxVel:
				self.setVel = self.maxVel

		# Decrease and increase angular velocity (X and B button on joystick)
		if self.joy.buttons[2]:
			self.rotVel = self.rotVel -  0.05* self.dt
			if self.rotVel < 0:
				self.rotVel = 0
		elif self.joy.buttons[1]:
			self.rotVel = self.rotVel + 0.05* self.dt
			if self.rotVel > self.maxRotVel:
				self.rotVel = self.maxRotVel
		
		#print(self.rotVel)
		

		# Check if deadman switch is pressed on gamepad
		deadman_switch = self.joy.buttons[5]
		#print(deadman_switch)
		if deadman_switch:
			# Linear velocity
			linear_velocity = self.joy.axes[4] * self.setVel
			#print(linear_velocity)
			# Angular velocity
			angular_velocity = self.joy.axes[3] * self.rotVel
			# Move track with constant linear velocity
			start_movement_btn = self.joy.buttons[4]
			if start_movement_btn==1 and self.start_movement_btn_old==0:
				self.linear_movement = not(self.linear_movement)
			self.start_movement_btn_old = start_movement_btn
		else:
			linear_velocity = 0
			angular_velocity = 0
			
			start_movement_btn = self.joy.buttons[4]
			if start_movement_btn==1 and self.start_movement_btn_old==0:
				self.linear_movement = False
			self.start_movement_btn_old = start_movement_btn
			

		# Check if constant movement is active
		if self.linear_movement:
			linear_velocity = self.setVel

		# Measuring cycle time
		self.dt = time.time() - self.start_time
		# Save current time
		self.start_time = time.time()

		# Send timestamp
		self.twist.header.stamp = rospy.get_rostime()
		# Send velocity to PLC
		self.twist.twist.linear.x = linear_velocity
		self.twist.twist.angular.z = angular_velocity

		#print(self.twist.twist)

		self.pub.publish(self.twist)
		
		self.pub = rospy.Publisher(self.topicName, TwistStamped,queue_size=1)



if __name__ == '__main__':
	rospy.set_param('/tracks_max_vel', 0.2)
	rospy.set_param('/tracks_max_rot_vel', 0.1)

	# Call class
	# Set limits in x, y, z direction and also rotation around z axis
	joy_control = joystick_control()
	rate = rospy.Rate(500)

	while not rospy.is_shutdown():
		joy_control.generate_points()
		rate.sleep()
