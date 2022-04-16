#!/usr/bin/env  python3
import rospy
#from std_msgs.msg import String
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import numpy as np
import time

from supportingFunctions.inverseKinematics_Phi import deltaInverseKin


# Regulator parameters:
Kp_1 = 5
Kp_4 = 2
Kp_5 = 3
Kp = np.array([Kp_1, Kp_1, Kp_1, Kp_4, Kp_5])
Kd_1 = 5
Kd_4 = 4
Kd_5 = 4
Kd = np.array([Kd_1, Kd_1, Kd_1, Kd_4, Kd_5])
maxOmega_1 = 50
maxOmega_3 = 250
maxOmegas = np.array([maxOmega_1, maxOmega_1, maxOmega_1, maxOmega_3, maxOmega_3])


# Names
nodeName = 'control_r2omegas'
topicName_r_control = 'r_control'
#topicName_alphas_actual = 'alphas_actual'
topicName_alphas_actual = 'PLC_comm_pub'
topicName_omegas_control = 'omegas_control'



# Global variables
r_control = np.zeros((5), dtype=np.float32)
r_control_Recieved = False
r_control_Recieved_Time = time.time()
r_control_timeout = 0.05	# in seconds
send_zero_omegas = 0


timer1 = time.time()



# TODO: save error for differential term
e_old = 0


def pretty_np(preprintString, numpyArray, nDecimals=2):
	displayPrint = preprintString
	for number in numpyArray:
		displayPrint += '	{num:.0{prec}f}'.format(num=number, prec=nDecimals)
	return displayPrint


def callback_recieveReference(data):
	global r_control
	global r_control_Recieved
	global r_control_Recieved_Time
	global send_zero_omegas

	r_control = data.data
	r_control_Recieved = True
	r_control_Recieved_Time = time.time()

	send_zero_omegas = 0

	return


def callback_control(data):

	global e_old
	global timer1

	global send_zero_omegas
	global r_control_Recieved
	if r_control_Recieved and time.time() - r_control_Recieved_Time > r_control_timeout:
		r_control_Recieved = False
		send_zero_omegas = 5


	# # Only for testing:
	# r_control = np.array([100, 0, -550, 30, 0])
	# r_control_Recieved = 1



	if r_control_Recieved == True:
		alphas_actual = data.data

		alphas_reference = np.zeros((5)) 

		alphas_ref_radians, _ = deltaInverseKin(r_control[0], r_control[1], r_control[2], r_control[3])
		alphas_reference[:3] = 180/np.pi*alphas_ref_radians

		alphas_reference[3:] = r_control[3:]

		# angular error - joint coordinates
		e = alphas_reference - alphas_actual[:5]
		de = e - e_old

		omegas_control = np.zeros((5), dtype=np.float32)
		omegas_control[:] = Kp*e + Kd * de

		omegas_control = np.clip(omegas_control, -maxOmegas, maxOmegas)
		omegas_control = omegas_control.astype(np.float32)

		e_old = e

		pub.publish(omegas_control)

		print('_________________________________________')
		print('Frequency: {:.02f}'.format(1/(time.time() - timer1)   ))

		timer1 = time.time()

		print(pretty_np('alphas ref:', alphas_reference))
		print(pretty_np('alphas act:', alphas_actual))
		print('-	-	-	-	-	-	-')
		print(pretty_np('\tP:', Kp*e, 4))
		print(pretty_np('\tD:', Kd*de, 4))
		print(pretty_np('omegas_ctrl', omegas_control))

	else:

		if send_zero_omegas > 0:
			omegas_control = np.zeros((5), dtype=np.float32)
			pub.publish(omegas_control)
			send_zero_omegas -= 1

			print(pretty_np('omegas_ctrl', omegas_control))







pub = rospy.Publisher(topicName_omegas_control, numpy_msg(Floats),queue_size=10)

rospy.init_node(nodeName, anonymous=False)

rospy.Subscriber(topicName_r_control, Floats, callback_recieveReference)
rospy.Subscriber(topicName_alphas_actual, Floats, callback_control)


rospy.spin()

