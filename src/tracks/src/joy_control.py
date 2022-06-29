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
		
		self.start_movement_btn_old = 0
		self.linear_movement = False

		# User settings:
		nodeName = 'track_joy_control'
		self.topicName = '/tracks/cmd'

		rospy.init_node(nodeName)

		self.pub = rospy.Publisher(self.topicName, numpy_msg(Floats),queue_size=1)

	def callback_joy(self, data):
		self.joy = data

	def generate_points(self):
		# Determine velocities in all directions
		# Decrease and increase velocity
		if self.joy.buttons[6]:
			self.setVel = self.setVel - 10 * self.dt
			if self.setVel < 1:
				self.setVel = 1
		elif self.joy.buttons[7]:
			self.setVel = self.setVel + 10 * self.dt
			if self.setVel > self.maxVel:
				self.setVel = self.maxVel
		
		print(self.setVel)
		

		# Check if deadman switch is pressed on gamepad
		deadman_switch = self.joy.buttons[5]
		#print(deadman_switch)
		if deadman_switch:
			# Linear velocity
			linear_velocity = self.joy.axes[1] * self.setVel
			# Angular velocity
			angular_velocity = self.joy.axes[0] * self.rotVel
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
		
		self.pub = rospy.Publisher(self.topicName, numpy_msg(Floats),queue_size=1)



if __name__ == '__main__':
	rospy.set_param('/tracks_max_vel', 50)
	rospy.set_param('/tracks_max_rot_vel', 50)

	# Call class
	# Set limits in x, y, z direction and also rotation around z axis
	boundries = [[-300, 300], [-300, 300], [-850, -500], [-180, 180] ]
	joy_control = joystick_control(boundries=boundries)
	rate = rospy.Rate(500)

	while not rospy.is_shutdown():
		joy_control.generate_points()
		rate.sleep()
