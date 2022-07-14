#!/usr/bin/env python3


'''
	Matic Vodopivec
	8.7.2022

	Help:
	Read data from sick scanner LMS111 and transform it to robot coordinate system.
    Cut data we don't need (at the edges of the field of view)

'''

from distutils.command.clean import clean
import sensor_msgs.point_cloud2 as pc2
import rospy
from sensor_msgs.msg import PointCloud2, LaserScan, PointCloud
import laser_geometry.laser_geometry as lg
import math
import tf2_ros
import tf
import numpy as np

rospy.init_node("laserscan_to_pointcloud")

lp = lg.LaserProjection()
#pc2_msg = PointCloud2()

pc_pub = rospy.Publisher("/robot_cloud", PointCloud, queue_size=1)

listener2 = tf.TransformListener()



def scan_cb(msg):
    # convert the message of type LaserScan to a PointCloud2
    #pc2_msg = lp.projectLaser(msg) #, channel_options=)
    pc2_msg = msg
    #pc2_msg.header.frame_id = 'world'

    # now we can do something with the PointCloud2 for example:
    # publish it
    #pc_pub.publish(pc2_msg)
    
    # convert it to a generator of the individual points
    point_generator = pc2.read_points(pc2_msg)
    #print(point_generator)

    # we can access a generator in a loop
    sum = 0.0
    num = 0
    for point in point_generator:
        if not math.isnan(point[2]):
            sum += point[2]
            num += 1
    # we can calculate the average z value for example
    #print(str(sum/num))

    # or a list of the individual points which is less efficient
    point_list = pc2.read_points_list(pc2_msg)
    #print(len(point_list))
    #print(point_list[0][0])
    
    world_points = PointCloud()
    world_points.header = pc2_msg.header
    world_points.points = point_list

    transformed_cloud = listener2.transformPointCloud('robot',world_points)
    #pc_pub.publish(transformed_cloud)
    #print(pc22)
    

    cleaned_points = []
    # Delete points where x is larger or smaller than our boundries
    for idx,i in enumerate(transformed_cloud.points):
        
        if i.y < -0.23: #or i.y > 0.2:
            #print(i.x)
            cleaned_points = np.append(cleaned_points, idx)
        
        if i.y > 0.26: #or i.y > 0.2:
            #print(i.x)
            cleaned_points = np.append(cleaned_points, idx)

    cleaned_points = cleaned_points.astype(int)
    
    #print("Original")
    #print(transformed_cloud.points[0])
    #print("Cleaned")
    transformed_cloud.points = np.delete(transformed_cloud.points, cleaned_points, axis=0)
    #print(transformed_cloud.points[0])

    #send_points = PointCloud()
    #send_points.header = pc2_msg.header
    #send_points.points = cleaned_points

    pc_pub.publish(transformed_cloud)
    

        
rospy.Subscriber("/cloud", PointCloud2, scan_cb, queue_size=1)
#rospy.Subscriber("/scan", LaserScan, scan_cb, queue_size=1)
rospy.spin()
