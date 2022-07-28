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
import matplotlib.pyplot as plt


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
		self.search_radius = z_par[3]

		self.y_minus_limit = y_limit[0]
		self.y_plus_limit  = y_limit[1]
		
		rospy.init_node("detect_asparagus", anonymous=True)
		# Subscribe to point cloud topic
		rospy.Subscriber(topic, PointCloud, self.callback_pointcloud, queue_size=1)
		# Get current pose of the track robot (calculation is not real time so we need location of the platform when data was acquired)
		rospy.Subscriber("/tracks/pose", Pose2D, self.callback_track_pose)
		self.pub = rospy.Publisher("/aspragus_cloud", PointCloud, queue_size=1)

		self.listener = tf.TransformListener()

		self.xyz = np.array([[0,0,0]])
		self.asparagus_points_arr = np.array([[0,0,0]])

		self.start_search = False

	def callback_track_pose(self, data):
		self.track_pose = data

	def callback_pointcloud(self, data):
		self.pointcloud = data.points

		# Cut points if y and z direction
		asparagus_points = self.find_z_points()

		if len(asparagus_points) > 0:
			self.point_histogram(asparagus_points, 0.02, 0.02, 20)

		robot_points = PointCloud()
		robot_points.header.stamp = rospy.Time.now()
		robot_points.header.frame_id = 'global'
		robot_points.points = asparagus_points

		#transformed_cloud = self.listener.transformPointCloud('global',robot_points)

		self.pub.publish(robot_points)

	def find_z_points(self):
		
		asparagus_points = []

		# Go through all points
		for i in self.pointcloud:
			# Check only for points there limited by Y cooridinate (to eliminate tracks)
			if i.y > self.y_minus_limit and i.y < self.y_plus_limit:
				# Search for point at specified Z range
				if i.z > self.min_z:
					if i.z < 0.10:
						asparagus_points = np.append(asparagus_points, i)

		return asparagus_points

	def point_histogram(self, asparagus_points, dx, dy, min_points):
		# Transform data to np.array
		for idx,i in enumerate(self.pointcloud):
			if idx == 0:
				self.xyz = [[i.x,i.y,i.z]]
			else:
				self.xyz = np.append(self.xyz,[[i.x,i.y,i.z]], axis = 0)

		# Create a grid matrix for z values
		min_val = np.min(self.xyz, axis=0)
		#print(min_val)
		max_val = np.max(self.xyz, axis=0)

		num_of_steps_x = int(np.ceil((max_val[0] - min_val[0]) / dx))
		num_of_steps_y = int(np.ceil((self.y_plus_limit - self.y_minus_limit) / dy))

		x_bins = np.linspace(min_val[0], max_val[0], num_of_steps_x)
		y_bins = np.linspace(self.y_minus_limit, self.y_plus_limit , num_of_steps_y)


		grid = np.zeros((num_of_steps_x, num_of_steps_y))

		# Check in which field are points
		x1 = []
		y1 = []
		for i in asparagus_points:
			x = i.x - min_val[0]
			y = i.y - min_val[1]

			x1 = np.append(x1, i.x)
			y1 = np.append(y1, i.y)

			field_x = int(np.floor(x / dx))
			field_y = int(np.floor(y / dy))

			grid[field_x, field_y] = grid[field_x, field_y] + 1

			#print("x = ", field_x, "y = ", field_y)
			#print(grid[field_x, field_y])
		
		#print(grid)
		grid = np.transpose(grid)
		

		#np.save("grid", grid)

		fig, ax = plt.subplots(figsize =(10, 7))
		# Creating plot
		h, xedges, yedges, img = plt.hist2d(x1, y1, bins =[x_bins, y_bins], cmin=min_points)
		#print(xedges)
		#print(yedges)
		#print(h.shape)
		#h, xedges, yedges = np.histogram2d(x1, y1, bins =[x_bins, y_bins])

		
		try:
			#hist = np.where(h < min_points, 0, h)
			x_idx, y_idx = np.where(h >= min_points)
			#print("x_idx = ", x_idx, "y_idx = ", y_idx)
			
			# Find boxes where maximus are present
			num_of_asparagus = len(x_idx)
			limit_array = np.zeros((num_of_asparagus, 4))

			for i in range(num_of_asparagus):
				# Lower limit in x direction
				limit_array[i,0] = xedges[x_idx[i]]
				# Upper limit in x direction
				limit_array[i,1] = xedges[x_idx[i]+1]
				# Lower limit in y direction
				limit_array[i,2] = yedges[y_idx[i]]
				# Upper limit in y direction
				limit_array[i,3] = yedges[y_idx[i]+1]

			print(limit_array)
		except:
			pass
		

		
		#plt.plot(hist)



		#hist, xedges, yedges = np.histogram2d(x1, y1, bins =[x_bins, y_bins])
		#print("h = ", h)
		#print("img = ", img)
		#print("Bars = ", bars)

		#plt.hexbin(x1, y1, bins =[x_bins, y_bins])
		plt.title("Histogram of Z coordinates")

		# Adding color bar
		plt.colorbar()
		
		ax.set_xlabel('X-axis') 
		ax.set_ylabel('Y-axis') 
		
		# show plot
		plt.tight_layout() 
		plt.savefig("Test")

	def circle_algorithm(self, asparagus_points):
		# Start searching for points in defined Z range

		# Find heighest point in array
		# Transform data to np.array
		for idx,i in enumerate(asparagus_points):
			if idx == 0:
				self.asparagus_points_arr = [[i.x,i.y,i.z]]
			else:
				self.asparagus_points_arr = np.append(self.asparagus_points_arr,[[i.x,i.y,i.z]], axis = 0)

		# Create a grid matrix for z values
		max_val = np.max(self.asparagus_points_arr, axis=0)		

		if max_val[2] >= self.start_z:
			self.start_search = True
		else:
			self.start_search = False

		# Init par
		z_search = self.min_z

		while z_search > self.min_z:
			#print("z_search = ", z_search)

			# Set limits in Z direction where we are searching for points inside of current step
			z_up_limit = z_search + (self.step_z) / 2
			z_down_limit = z_search - (self.step_z) / 2


if __name__ == "__main__":
	# Call class
	#topic = "/intel_l515_global_cloud"
	topic = "/scanner_3D_img"
	start_z = 0.25
	step_z = 0.01
	min_z = 0.02
	search_radius = 0.05

	z_par = [start_z, step_z, min_z, search_radius]
	
	y_plus_limit = 0.3
	y_minus_limit = -0.3
	y_limit = [y_minus_limit, y_plus_limit]

	detector = detect_asparagus(topic=topic, z_par=z_par, y_limit=y_limit)
	rospy.spin()