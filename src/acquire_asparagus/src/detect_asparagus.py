#!/usr/bin/env python3


'''
	Matic Vodopivec
	21.7.2022

	Help:
	Detect asparagus from pointcloud

'''

from pickle import TRUE
import rospy
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Pose2D
import math
import tf2_ros
import tf
import numpy as np
import time
import matplotlib.pyplot as plt
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats


class detect_asparagus:
	def __init__(self, topic, z_par, y_limit, display_results):
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

		self.display_results = display_results
		
		rospy.init_node("detect_asparagus", anonymous=True)
		# Subscribe to point cloud topic
		rospy.Subscriber(topic, PointCloud, self.callback_pointcloud, queue_size=1)
		# Get current pose of the track robot (calculation is not real time so we need location of the platform when data was acquired)
		rospy.Subscriber("/tracks/pose", Pose2D, self.callback_track_pose)
		self.pub = rospy.Publisher("/aspragus_cloud", PointCloud, queue_size=1)
		self.asparagus_location_pub = rospy.Publisher("/aspragus_locations", numpy_msg(Floats), queue_size=1)

		self.listener = tf.TransformListener()

		self.xyz = np.array([[0,0,0]])
		self.asparagus_points_arr = np.array([[0,0,0]])

		self.start_search = False

		self.median_available = False

		self.first_pick_point = True


	def callback_track_pose(self, data):
		self.track_pose = data

	def callback_pointcloud(self, data):
		
		self.start_time = time.time()

		self.pointcloud = data.points

		# Cut points in y and z direction (clean ground points and robot frame)
		cut_z_height = 0.1 # in meters
		self.asparagus_points = self.find_z_points(cut_z_height)

		

		# Check if there are any points above ground
		if len(self.asparagus_points) > 0:
			# Size of square for decimation
			dx = dy = 0.03
			# Minimal number of points in square
			min_points = 27
			# Plot 2D histogram
			plot_results = False
			# Return sqares in which there are more than min_points
			limit_array, points_valid = self.point_histogram(self.asparagus_points, 0.02, 0.02, min_points, plot_results)

			# Check if any sqares are valid
			if points_valid:
				z_pick_height = 0.04
				# Minimal number ob points below z_pick_height
				min_z_points = 5

				# Calculate mean value for each asparagus
				x_median, y_median = self.median_asparagus_points(self.asparagus_points, limit_array, z_pick_height, min_z_points)

				#print("Find x,y time = ", time.time() - self.start_time)

		# Check if median median for predicted aspragus is calculated
		if self.median_available:
			search_radius = 0.03
			harvest_height = 0.15
			harvest_point_valid = self.check_asparagus_height(x_median, y_median, search_radius, harvest_height)

			# Transform pick points to robot coordinate system
			frame_id = 'robot'
			self.transform_pick_points(frame_id, x_median, y_median, harvest_point_valid, z_pick_height)


	def find_z_points(self, cut_z_height):
		
		asparagus_points = []

		# Go through all points
		for i in self.pointcloud:
			# Check only for points there limited by Y cooridinate (to eliminate tracks)
			if i.y > self.y_minus_limit and i.y < self.y_plus_limit:
				# Search for point at specified Z range
				if i.z > self.min_z:
					if i.z < cut_z_height:
						asparagus_points = np.append(asparagus_points, i)

		return asparagus_points

	def point_histogram(self, asparagus_points, dx, dy, min_points, display_results=False):
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
		
		# Set bin limits
		x_bins = np.linspace(min_val[0], max_val[0], num_of_steps_x)
		y_bins = np.linspace(self.y_minus_limit, self.y_plus_limit , num_of_steps_y)

		x1 = []
		y1 = []
		for i in asparagus_points:
			# Get x and y points
			x1 = np.append(x1, i.x)
			y1 = np.append(y1, i.y)

		
		# Creating plot
		if display_results:
			fig, ax = plt.subplots(figsize =(10, 6))
			h, xedges, yedges, _ = plt.hist2d(x1, y1, bins =[x_bins, y_bins], cmin=min_points)
		else:
			h, xedges, yedges = np.histogram2d(x1, y1, bins =[x_bins, y_bins])
		#print(xedges)
		#print(yedges)
		#print(h.shape)
		#h, xedges, yedges = np.histogram2d(x1, y1, bins =[x_bins, y_bins])

		try:
			#hist = np.where(h < min_points, 0, h)
			x_idx, y_idx = np.where(h >= min_points)
			#print("x_idx = ", x_idx, "y_idx = ", y_idx)
			
			# Find boxes where maximums are present
			num_of_asparagus = len(x_idx)
			limit_array = np.zeros((num_of_asparagus, 4))

			points_valid = True

			for i in range(num_of_asparagus):
				# Lower limit in x direction
				limit_array[i,0] = xedges[x_idx[i]]
				# Upper limit in x direction
				limit_array[i,1] = xedges[x_idx[i]+1]
				# Lower limit in y direction
				limit_array[i,2] = yedges[y_idx[i]]
				# Upper limit in y direction
				limit_array[i,3] = yedges[y_idx[i]+1]

			#print(limit_array)
		except:
			limit_array = np.zeros((1, 4))
			points_valid = False
		

		if display_results:
			
			#plt.hexbin(x1, y1, bins =[x_bins, y_bins])
			plt.title("Histogram of Z coordinates")

			# Adding color bar
			plt.colorbar()
			
			ax.set_xlabel('X-axis') 
			ax.set_ylabel('Y-axis') 
			
			# show plot
			plt.tight_layout() 
			plt.savefig("2D point histogram")

		return limit_array, points_valid

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

	def median_asparagus_points(self, asparagus_points, limit_array, z_pick_height, min_z_points):
		num_of_asparagus = limit_array.shape[0]

		#box_points_arr = np.zeros((1, 3))
		box_points_arr = [[] for _ in range(num_of_asparagus)]
		x_box = [[] for _ in range(num_of_asparagus)]
		y_box = [[] for _ in range(num_of_asparagus)]
		z_box = [[] for _ in range(num_of_asparagus)]
		
		for i in asparagus_points:
			#print(i)
			for j in range(num_of_asparagus):
				if i.x >= limit_array[j,0] and i.x < limit_array[j,1] and i.y >= limit_array[j,2] and i.y < limit_array[j,3]:
					#box_points_arr[j] = np.append(box_points_arr[j], [[i.x,i.y,i.z]], axis = 0)
					point = [i.x, i.y, i.z]
					box_points_arr[j].append(point)
					x_box[j].append(i.x)
					y_box[j].append(i.y)
					z_box[j].append(i.z)

		
		# Check if there points bellow z pick height
		num_of_pick_points = np.zeros(num_of_asparagus)
		for j in range(num_of_asparagus):
			for z in z_box[j]:
				if z < z_pick_height:
					num_of_pick_points[j] = num_of_pick_points[j] + 1

		#print(num_of_pick_points)

		# Find x and y median for all blobs
		x_median_arr = []
		y_median_arr = []
		for j in range(num_of_asparagus):
			x_median = np.median(x_box[j])
			y_median = np.median(y_box[j])

			if num_of_pick_points[j] >= min_z_points:
				x_median_arr.append(x_median)
				y_median_arr.append(y_median)

		#print("x median = ", x_median_arr)
		#print("y median = ", y_median_arr)

		if len(x_median_arr) > 0:
			self.median_available = True
		else:
			self.median_available = False

		return x_median_arr, y_median_arr

	def check_asparagus_height(self, x_median, y_median, search_radius, harvest_height):
		
		# Check if asparagus is high enough for harvesting
		harvest_point_valid = np.zeros(len(x_median))

		for j in range(len(x_median)):
			for i in self.pointcloud:
				if (i.x - x_median[j])**2 + (i.y - y_median[j])**2 < search_radius**2:
					if i.z >= harvest_height:
						harvest_point_valid[j] = 1
						#print(i.z)
						break
		
		#print("x_median = ", x_median)
		#print("y_median = ", y_median)
		#print(harvest_point_valid)

		return harvest_point_valid

	def transform_pick_points(self, frame_id, x_median, y_median, harvest_point_valid, z_pick_height):

		robot_points = PointCloud()
		robot_points.header.stamp = rospy.Time.now()
		robot_points.header.frame_id = 'global'
		
		#invalid_points = np.where(harvest_point_valid == 0)

		#print(invalid_points[0])
		#if len(invalid_points[0]) > 0:
		#	x_median = np.delete(x_median, invalid_points[0])
		#	y_median = np.delete(y_median, invalid_points[0])

		# Number of aspargus ready for picking
		num_of_pick_asparagus = len(x_median)
		#pick_points = np.zeros((num_of_pick_asparagus,3))
		
		
		#self.aspargus = []
		new_point = False
		if self.first_pick_point:
			# This is the first pick point
			self.aspargus = np.array([[x_median[0], y_median[0], z_pick_height, harvest_point_valid[0]]])
			self.first_pick_point = False
		else:
			for idx in range(num_of_pick_asparagus):
				new_point = False
				# Calculate all distances to valid points
				dist_array = np.zeros(len(self.aspargus))
				new_point_arr = np.full((len(self.aspargus)), False)
				for idx2, i in enumerate(self.aspargus):
					point1 = np.array([x_median[idx], y_median[idx], 0])
					point2 = np.array([i[0], i[1], 0])
					dist = np.linalg.norm(point1 - point2)

					if dist > 0.03:
						# new point potencial
						new_point_arr[idx2] = True
					else: 
						# fix point location
						self.aspargus[idx2] = np.array([[x_median[idx], y_median[idx], z_pick_height, harvest_point_valid[idx]]])
						new_point_arr[idx2] = False

					dist_array[idx2] = dist

				print('new_point_arr = ', new_point_arr)
				new_point = np.all(new_point_arr == True)
				print('new_point = ', new_point)
				print('dist array = ', dist_array)

				if new_point:
					self.aspargus = np.append(self.aspargus,[[x_median[idx], y_median[idx], z_pick_height, harvest_point_valid[idx]]], axis = 0)
		print('self.aspargus = ',self.aspargus)
		'''
		for idx in range(num_of_pick_asparagus):
			# Check if point was already saved
			new_point = False
			if self.first_pick_point == False:

				new_point_arr = np.full((len(self.aspargus)), False)
				for idx2,i in enumerate(self.aspargus):
					point1 = [x_median[idx], y_median[idx], 0]
					point2 = [i[0], i[1], 0]
					dist = np.linalg.norm(point1 - point2)

					if dist > self.search_radius:
						new_point = True
					else:
						new_point = False
						break

					if (x_median[idx] - i[0])**2 + (y_median[idx] - i[1])**2 > self.search_radius**2:
						new_point_arr[idx2] = True
					else:
						# Fix point position
						self.aspargus[idx2] = np.array([[x_median[idx], y_median[idx], z_pick_height, harvest_point_valid[idx]]])

				# Check if all true -> than we have new point
				new_point = np.all(new_point_arr == True)
			else:
				self.first_pick_point = False
				self.aspargus = np.array([[x_median[idx], y_median[idx], z_pick_height, harvest_point_valid[idx]]])
				#print(self.aspargus)
				
			if new_point:
				self.aspargus = np.append(self.aspargus,[[x_median[idx], y_median[idx], z_pick_height, harvest_point_valid[idx]]], axis = 0)
		'''
		
		# Save points in PointCloud format so that we can visualize them in rviz
		num_of_pick_asparagus = len(self.aspargus)
		
		if num_of_pick_asparagus > 0:
			if self.display_results:
				pick_points = self.pointcloud[:num_of_pick_asparagus]
				for idx, i in enumerate(self.aspargus):
					# Save x coordinate
					x_trans = self.track_pose.x * math.cos(self.track_pose.theta)
					y_trans = self.track_pose.y * math.sin(self.track_pose.theta)

					# Transform points from global cs to robot cs
					pick_points[idx].x = i[0] #- x_trans
					pick_points[idx].y = i[1] #- y_trans
					pick_points[idx].z = i[2]

				robot_points.points = pick_points

				self.pub.publish(robot_points)

			#transformed_cloud = self.listener.transformPointCloud('robot',robot_points)

			#print(transformed_cloud.points)

			# Filter duplicated points 
			filtered_points = self.filter_pick_points(0.03)

			flatten_aspargus = np.asarray(filtered_points, dtype=np.float32)
			flatten_aspargus = flatten_aspargus.flatten()

			print(self.aspargus)
			print('Filtered points = ', filtered_points)

			self.asparagus_location_pub.publish(flatten_aspargus)
			print("Elapsed time = ", time.time() - self.start_time)

	def filter_pick_points(self, min_dist):
		pick_points_0 = np.copy(self.aspargus)
		#print('test = ', self.aspargus)

		numOfAsparagus = len(pick_points_0)
		#print('Pick_points = ',pick_points_0)
		#print('Num of as = ',numOfAsparagus)

		if numOfAsparagus > 1:
			dist_matrix = np.zeros(())

			#idx = 0
			for idx, i in enumerate(pick_points_0):
				dist_array = np.zeros(len(pick_points_0))
				for idx2, j in enumerate(pick_points_0):
					if idx == idx2:
						dist_array[idx] = 0
					else:
						dist = np.linalg.norm(i[:3] - j[:3])
						dist_array[idx2] = dist
				
				#print('Dist = ', dist_array)

				delete_arr = []
				for idx3, k in enumerate(dist_array):
					if k < min_dist and idx3 != idx:
						delete_arr.append(idx3)
				pick_points_0 = np.delete(pick_points_0, delete_arr, axis=0)

				#print('Dist2 = ', pick_points_0)


				

		return pick_points_0




		
			


if __name__ == "__main__":
	# Call class
	#topic = "/intel_l515_global_cloud"
	topic = "/scanner_3D_img"
	start_z = 0.25
	step_z = 0.01
	min_z = 0.02
	search_radius = 0.01

	z_par = [start_z, step_z, min_z, search_radius]
	
	y_plus_limit = 0.3
	y_minus_limit = -0.3
	y_limit = [y_minus_limit, y_plus_limit]

	display_results = True

	detector = detect_asparagus(topic=topic, z_par=z_par, y_limit=y_limit, display_results=display_results)
	rospy.spin()