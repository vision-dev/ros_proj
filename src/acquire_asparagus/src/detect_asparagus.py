#!/usr/bin/env python3


'''
	Matic Vodopivec
	21.7.2022

	Help:
	Detect asparagus from pointcloud

'''


import rospy
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Pose2D
import math
import tf2_ros
import tf
import numpy as np
import time

class detect_asparagus:
	def __init__(self, topic, z_par, y_limit):
		'''
		Inputs:
			- topic (string) = name of the topic of the pointcloud in robot coordinates
			- z_par (array3)  = parameters for searchnig points in Z direction [start_z, step_z, min_z]
				- start_z = heighest point to start searching for asparagus (should be shortest asparagus height we still need to harvest)
				- step_z  = step to go down in z direction
				- min_z   = height at which we stop searching
			- y_limit (array2) = limits in y minus and y plus direction [y_minus_limit, y_plus_limit]
		'''

		self.start_z = z_par[0]
		self.step_z  = z_par[1]
		self.min_z   = z_par[2]
		self.y_minus_limit = y_limit[0]
		self.y_plus_limit  = y_limit[1]
		
		rospy.init_node("detect_asparagus", anonymous=True)
		# Subscribe to point cloud topic
		rospy.Subscriber(topic, PointCloud, self.callback_pointcloud, queue_size=1)
		# Get current pose of the track robot (calculation is not real time so we need location of the platform when data was acquired)
		rospy.Subscriber("/tracks/pose", Pose2D, self.callback_track_pose)
		self.pub = rospy.Publisher("/aspragus_cloud", PointCloud, queue_size=1)

	def callback_track_pose(self, data):
		self.track_pose = data

	def callback_pointcloud(self, data):
		self.pointcloud = data.points

		asparagus_points = self.find_z_points()

		robot_points = PointCloud()
		robot_points.header.stamp = rospy.Time.now()
		robot_points.header.frame_id = 'robot'
		robot_points.points = asparagus_points
		self.pub.publish(robot_points)

	def find_z_points(self):
		# Start search for points at start z poz
		z_search = self.start_z

		first_point = True
		center_point = np.zeros((10,2))

		# calculate number of points of asparagus based on step_z size
		numOfSteps = (self.start_z - self.min_z) / self.step_z
		asparagus_points = []#np.zeros((10, int(numOfSteps)))
		#print(numOfSteps)

		current_z_step = 0
		numOfAsparagus = 0
		while z_search > self.min_z:
			#print("z_search = ", z_search)

			z_up_limit = z_search + 0.001
			z_down_limit = z_search - 0.001

			idx = 0
			center_point_set = np.zeros(10)

			for i in self.pointcloud:
				point_in_circle = False
				# Check only for points there limited by Y cooridinate (to eliminate tracks)
				if i.y > self.y_minus_limit and i.y < self.y_plus_limit:
					# Search for point at specified Z coordinates
					if i.z > z_down_limit and i.z < z_up_limit:
						# Find all asparagus at start z height
						if first_point:
							numOfAsparagus = 1

						
						for j in range(numOfAsparagus):
							
							# Search in circle
							if (i.x - center_point[j][0])**2 + (i.y - center_point[j][1])**2 < 0.03**2 or first_point:
								first_point = False

								point_in_circle = True
								
								asparagus_points = np.append(asparagus_points, i)

								if center_point_set[j] == 0:
									center_point_set[j] = 1

									

									# Set search range for next point
									
									center_point[j][0] = i.x
									center_point[j][1] = i.y

									#print(center_point[j])
									#print(z_search)
								
								
								
							
						if point_in_circle == False:
							# Save new center point
							center_point[numOfAsparagus][0] = i.x
							center_point[numOfAsparagus][1] = i.y
							
							numOfAsparagus = numOfAsparagus + 1
						else:
							continue
						
			if numOfAsparagus >= 0:
				z_search = z_search - self.step_z
				center_point_set = np.zeros(10)
				current_z_step = current_z_step + 1
			else:
				break


		#print(asparagus_points)
		#print(numOfAsparagus)
		return asparagus_points



if __name__ == "__main__":
	# Call class
	topic = "/intel_l515_global_cloud"
	start_z = 0.25
	step_z = 0.005
	min_z = -0.02

	z_par = [start_z, step_z, min_z]
	
	y_plus_limit = 0.2
	y_minus_limit = -0.15
	y_limit = [y_minus_limit, y_plus_limit]

	detector = detect_asparagus(topic=topic, z_par=z_par, y_limit=y_limit)
	rospy.spin()