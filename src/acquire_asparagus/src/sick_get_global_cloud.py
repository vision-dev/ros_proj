#!/usr/bin/env python3

'''
	Matic Vodopivec
	12.7.2022

	Help:
	- Read data from sick scanner transformed into world CS
	- Read pose from track robot
	- Assemble 3D image
'''

import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import PointCloud
import numpy as np
from geometry_msgs.msg import TransformStamped
from tf.transformations import quaternion_from_euler
import tf
from tf2_ros import TransformBroadcaster

class get_3D_sensor_img:
	def __init__(self):
		rospy.init_node('sensor_img')
		# Get pose 2D of the tracks
		rospy.Subscriber("/tracks/pose", Pose2D, self.read_track_pose)
		self.track_pose = Pose2D()
		self.save_poz = False
		# Get 3D point cloud from sick sensor in world CS
		rospy.Subscriber("/robot_cloud", PointCloud, self.get_world_point_cloud)
		self.current_point_cloud = PointCloud()
		self.scanner_cloud = []
		self.world_point_cloud = PointCloud()
		self.save_start_poz = False
		self.new_point_cloud = PointCloud()

		self.listener = tf.TransformListener()

		self.pc_pub = rospy.Publisher("/scanner_3D_img", PointCloud, queue_size=1)

		# Initialize the transform broadcaster
		self.br = tf.TransformBroadcaster()

	def read_track_pose(self, data):
		self.track_pose = data

	def get_world_point_cloud(self, data):
		# Read points in track coordinate system
		self.current_point_cloud = PointCloud()
		self.current_point_cloud = data

		# transform data to global CS
		try:
			self.world_point_cloud = self.listener.transformPointCloud('global',self.current_point_cloud)
		except:
			pass

		if self.save_poz == False:
			self.saved_track_pose = self.track_pose

			self.save_poz = True

		route_x = self.track_pose.x - self.saved_track_pose.x
		route_y = self.track_pose.y - self.saved_track_pose.y
		#print(route_x)

		self.new_point_cloud.header.stamp = rospy.Time.now()
		self.new_point_cloud.header.frame_id = 'global'

		# Save data to array each time track robot move for more than 1 mm
		if abs(route_x) > 0.001 or abs(route_y) > 0.001:
			self.scanner_cloud = np.append(self.scanner_cloud, self.world_point_cloud.points)
			#print(self.scanner_cloud)
			self.new_point_cloud.points = self.scanner_cloud

			#print(self.new_point_cloud.points)

			self.pc_pub.publish(self.new_point_cloud)

			self.save_poz = False


if __name__ == "__main__":
	# Call class
	sensor_img = get_3D_sensor_img()
	rospy.spin()
