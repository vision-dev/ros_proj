#!/usr/bin/env python3


'''
	Matic Vodopivec
	14.7.2022

	Help:
	Read data from intel D435i camera and transform it to global coordinate system

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
import time

rospy.init_node("intel_d435_to_pointcloud")

pc_pub = rospy.Publisher("/intel_d435_global_cloud", PointCloud, queue_size=1)

listener2 = tf.TransformListener()

def transform(msg):
    start_time = time.time()

    pc2_msg = msg
    
    
    # convert it to a generator of the individual points
    point_generator = pc2.read_points(pc2_msg)
    #print(point_generator)

    # or a list of the individual points which is less efficient
    point_list = pc2.read_points_list(pc2_msg)
    #print(len(point_list))
    #print(point_list[0][0])

    robot_points = PointCloud()
    robot_points.header = pc2_msg.header
    robot_points.points = point_list

    transformed_cloud = listener2.transformPointCloud('robot',robot_points)
    #pc_pub.publish(transformed_cloud)
    #print(pc22)
    
    
    cleaned_points = []
    # Delete points where x is larger or smaller than our boundries
    for idx,i in enumerate(transformed_cloud.points):
        
        if i.y < -0.20: #or i.y > 0.2:
            #print(i.x)
            cleaned_points = np.append(cleaned_points, idx)
        
        if i.y > 0.26: #or i.y > 0.2:
            #print(i.x)
            cleaned_points = np.append(cleaned_points, idx)

    cleaned_points = cleaned_points.astype(int)
    
    transformed_cloud.points = np.delete(transformed_cloud.points, cleaned_points, axis=0)

    

    pc_pub.publish(transformed_cloud)

    end = time.time()
    print(end - start_time)
    

        
rospy.Subscriber("/camera/depth/color/points", PointCloud2, transform, queue_size=1)
rospy.spin()
