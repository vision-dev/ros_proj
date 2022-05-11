#!/usr/bin/env  python3
from ast import If
from pickle import TRUE
import rospy
#from std_msgs.msg import String
from beckhoff_msgs.msg import array5
from beckhoff_msgs.msg import array6
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import numpy as np
import time

from supportingFunctions.inverseKinematics_Phi import deltaInverseKin

class omegas_control:
	def __init__(self, Kp, Kd, maxOmegas, displayResult=False):
		self.Kp = np.asarray(Kp)
		self.Kd = np.asarray(Kd)
		self.maxOmegas = np.asarray(maxOmegas)
		self.displayResult = displayResult

		self.e_old = 0.0

		# Define node and topics
		# Names
		self.nodeName = 'control_r2omegas'
		# Subscribing to topic
		self.topicName_r_control = '/r_control' # Calculate trajectory of delta robot
		# Subscribing to topic
		self.topicName_alphas_actual = '/alpha_delta' # Angles from servo and DC motors -> We get them from beckhoff PLC over ADS communication
		# Publishing topics 
		self.topicName_omegas_control = '/omegas_delta' # Sending motor velocities to PLC

	def pretty_np(self, preprintString, numpyArray, nDecimals=2):
		displayPrint = preprintString
		for number in numpyArray:
			displayPrint += '	{num:.0{prec}f}'.format(num=number, prec=nDecimals)
		return displayPrint

	def callback_readReference(self, data):
		self.r_control = data.data #np.asarray(data.data[:4])
		#print(self.r_control)
		#self.r_time = data.data[5]

		return

	def callback_control(self, data):
		# Check if we received new data from /r_control topic
		#if self.r_time != r_time_old:
		newData_flag = True

		#r_time_old = self.r_time

		if newData_flag:
			newData_flag = False
			# Read actual angles
			self.alphas_actual = data.data

			print(self.r_control)

			alphas_reference = np.zeros((5)) 

			alphas_ref_radians, _ = deltaInverseKin(self.r_control[0], self.r_control[1], self.r_control[2], self.r_control[3])
			alphas_reference[:3] = 180/np.pi*alphas_ref_radians

			alphas_reference[3:] = self.r_control[3:]

			# angular error - joint coordinates
			e = alphas_reference - self.alphas_actual
			de = e - self.e_old

			omegas_control = np.zeros((5), dtype=np.float32)
			omegas_control = self.Kp*e + self.Kd * de

			omegas_control = np.clip(omegas_control, -self.maxOmegas, self.maxOmegas)
			omegas_control = omegas_control.astype(np.float64)

			self.e_old = e

			time_ms = time.time()
			time_ms = time_ms.astype(np.float64)

			data_to_send = np.append(omegas_control, time_ms)

			self.pub.publish(data_to_send)

			# Display data
			if self.displayResult:

				print(self.pretty_np('alphas ref:', alphas_reference))
				print(self.pretty_np('alphas act:', self.alphas_actual))
				print('-	-	-	-	-	-	-')
				print(self.pretty_np('\tP:', self.Kp*e, 4))
				print(self.pretty_np('\tD:', self.Kd*de, 4))
				print(self.pretty_np('omegas_ctrl:', omegas_control))
	
	def topics(self):
		self.pub = rospy.Publisher(self.topicName_omegas_control, array6,queue_size=10)

		rospy.init_node(self.nodeName, anonymous=False)

		rospy.Subscriber(self.topicName_r_control, Floats, self.callback_readReference)
		rospy.Subscriber(self.topicName_alphas_actual, array5, self.callback_control)

		rospy.spin()


if __name__ == "__main__":

	Kp = [5,5,5,2,3]
	Kd = [5,5,5,4,4]
	maxOmega = [20,20,20,10,10]
	displayResults = True

	control = omegas_control(Kp, Kd, maxOmega, displayResults)

	control.topics()








