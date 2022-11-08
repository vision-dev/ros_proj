#!/usr/bin/env  python3
from ast import If
from pickle import TRUE
import rospy

# Include msg to communicate with robot
from beckhoff_msgs.msg import CmdRobot
from beckhoff_msgs.msg import JointStateRobot

from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import numpy as np
import time
import math
from std_msgs.msg import Float32

from supportingFunctions.inverseKinematics_Phi import deltaInverseKin

class velocity_control:
	def __init__(self, Kp, Kd, maxOmegas, displayResult=False):
		self.Kp = np.asarray(Kp)
		self.Kd = np.asarray(Kd)
		self.maxOmegas = np.asarray(maxOmegas)
		self.displayResult = displayResult

		self.dt    = 0.0
		self.e_old = 0.0
		self.Timestamp_old = 0
		self.newData_flag = False
		self.dqd = np.zeros((5)) 


		# Define node and topics
		# Names
		self.nodeName = 'control_r2omegas'
		# Subscribing to topic
		self.topicName_r_control = '/r_control' # Calculate trajectory of delta robot
		# Subscribing to topic
		self.topicName_delta_from_plc = '/robot/joint_state' # Angles from servo and DC motors -> We get them from beckhoff PLC over ADS communication
		# Publishing topics 
		self.topicName_delta_to_plc = '/robot/cmd' # Sending motor velocities to PLC

		rospy.init_node(self.nodeName, anonymous=False)

		rospy.Subscriber(self.topicName_r_control, Floats, self.callback_readReference, queue_size=1)
		rospy.Subscriber(self.topicName_delta_from_plc, JointStateRobot, self.callback_control)
		rospy.Subscriber("/robot/qd", Floats, self.callback_read_qd, queue_size=1)
		
		self.qd_available = False
		self.stevec = 0

	def pretty_np(self, preprintString, numpyArray, nDecimals=4):
		displayPrint = preprintString
		for number in numpyArray:
			displayPrint += '	{num:.0{prec}f}'.format(num=number, prec=nDecimals)
		return displayPrint

	def callback_readReference(self, data):
		self.r_control = data.data

		#print('r_control = ', self.r_control)

		self.start_time = time.time()
		#print(self.r_control)

		self.qd_available = False

		return

	def callback_read_qd(self, data):
		self.qd = data.data

		self.start_time = time.time()

		#print(self.qd)

		self.qd_available = True

		return

	def callback_control(self, data):
		# Check if we received new data from PLC
		#print(f"timestamp {repr(data)}")
		
		if data.Timestamp != self.Timestamp_old:
			self.newData_flag = True
		
		#print(data.Timestamp)

		if self.newData_flag:
			self.newData_flag = False
			#dt = (data.Timestamp - self.Timestamp_old)
			#print("delta stevec: " + str(dt))
			self.Timestamp_old = data.Timestamp

			# Read actual angles
			self.qq = [data.qq.j0, data.qq.j1, data.qq.j2, data.qq.j3, data.qq.j4]
			self.qq = np.asarray(self.qq, dtype=np.float32)
			# read actual velocity
			self.dq = [data.dq.j0, data.dq.j1, data.dq.j2, data.dq.j3, data.dq.j4]
			self.dq = np.asarray(self.dq, dtype=np.float32)

			#print(self.qq)

			# Desired axis velocity
			qd = np.zeros((5)) 
			# Desired axis velocity in radians
			omega = 3
			
			x_sin_test = 100*math.sin(time.time()*4)
			#print(x_sin_test)

			#print('r_control = ', self.r_control)

			if self.qd_available == False:
				qd_radians, _ = deltaInverseKin(self.r_control[0], self.r_control[1], self.r_control[2], self.r_control[3])
				#print('qd_radians = ', qd_radians)
				#qd_radians, _ = deltaInverseKin(x_sin_test, 0, -750, self.r_control[3])
				# Transform to degrees
				qd[:3] = 180/np.pi*qd_radians
				qd[3:] = self.r_control[3:]
			else:
				qd = self.qd

			#print("qd = ", qd)
			# test PD control
			'''
			self.stevec = self.stevec + 1			
			if self.stevec < 5000:
				aref = 10
			else:
				aref = 30
				if self.stevec > 10000:
					self.stevec = 0

			qd[0] = aref #15+10*math.sin(time.time()*2)
			qd[1] = 5 #
			qd[2] = 5 #
			'''
			

			#self.testpub.publish(qd[0])

			
			#print('qd = ', qd)
			#print("desired poz = ", qd)

			# angular error - joint coordinates
			e = qd - self.qq
			
			
			#de = (e - self.e_old) / self.dt
			#de = self.dqd - self.dq
			de = -self.dq
			
			#print(e)
			#print(self.e_old)

			#self.Kp = rospy.get_param('/robot_Kp')
			#self.Kd = rospy.get_param('/robot_Kd')
			#print(self.Kp)
			
			dq = np.zeros((5), dtype=np.float32)
			dq = self.Kp*e + self.Kd * de

			#if qd[4] == 0 or qd[4] == -120:
			#	dq[4] = 0
			
			# limit error for gripper
			#if e[4] < 1:
			#	dq[4] = 0

			dq = np.clip(dq, -self.maxOmegas, self.maxOmegas)
			dq = dq.astype(np.float32)

			# Save old error
			self.e_old = e
			# Save current time
			time_ms = time.time()
			# Calculate cycle time
			self.dt = time_ms - self.start_time

			#RobotCmd = np.zeros((6), dtype=np.float32)
			RobotCmd = CmdRobot()

			# Desired velocity
			self.dqd = dq

			#print(dq)

			# Write data to array
			RobotCmd.Timestamp = rospy.get_rostime()
			RobotCmd.dq.j0 = dq[0]
			RobotCmd.dq.j1 = dq[1]
			RobotCmd.dq.j2 = dq[2]
			RobotCmd.dq.j3 = dq[3]
			#RobotCmd.dq.j4 = dq[4]
			#print(self.r_control[4])
			if qd[4] == 0.0:
				RobotCmd.dq.j4 = 0
				# Open gripper
				RobotCmd.open_gripper  = 0
				RobotCmd.close_gripper = 1
			elif qd[4] == -120.0:
				RobotCmd.dq.j4 = 0
				# Open gripper
				RobotCmd.open_gripper  = 1
				RobotCmd.close_gripper = 0
			else:
				RobotCmd.dq.j4 = dq[4]
				RobotCmd.open_gripper  = 0
				RobotCmd.close_gripper = 0

			#print(RobotCmd)

			#print('Open gripper = ', RobotCmd.open_gripper)
			#print('Close gripper = ', RobotCmd.close_gripper)

			#print('--------------------------')
			#print(data_to_send)
			#print(str((self.dt)*1000) + ' ms')
			#print('--------------------------')

			self.pub.publish(RobotCmd)

			# Display data
			if self.displayResult:

				print(self.pretty_np('alphas ref:', qd))
				print(self.pretty_np('alphas act:', self.qq))
				print('-	-	-	-	-	-	-')
				print(self.pretty_np('\tP:', self.Kp*e, 4))
				print(self.pretty_np('\tD:', self.Kd*de, 4))
				print(self.pretty_np('omegas_ctrl:', dq))
	
	def topics(self):

		self.pub = rospy.Publisher(self.topicName_delta_to_plc, CmdRobot, queue_size=1)

		self.testpub = rospy.Publisher("test_data", Float32, queue_size=1)

		rospy.spin()


if __name__ == "__main__":
	
	
	Kp_delta = 5
	Kp = [Kp_delta,Kp_delta,Kp_delta, 2.5, 0.5]
	#rospy.set_param('/robot_Kp', [5,5,5,2,3])
	Kd_delta = 0.05
	Kd_DC = 0.05
	Kd = [Kd_delta, Kd_delta, Kd_delta, 0, 0]
	#rospy.set_param('/robot_Kd', [0.005,0.005,0.005,0.4,0.4])
	maxOmega = [150,150,150,250,250]
	displayResults = False

	control = velocity_control(Kp, Kd, maxOmega, displayResults)

	control.topics()








