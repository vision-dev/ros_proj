#!/usr/bin/env python3


'''
	Matic Vodopivec
	8.7.2022

	Help:
	Read data from sick scanner LMS111

'''

import sensor_msgs.point_cloud2 as pc2
import rospy
from sensor_msgs.msg import PointCloud2, LaserScan, PointCloud
import laser_geometry.laser_geometry as lg
import math
import tf2_ros
import tf
import numpy as np
from collections import namedtuple

rospy.init_node("laserscan_to_pointcloud")

lp = lg.LaserProjection()
#pc2_msg = PointCloud2()

pc_pub = rospy.Publisher("/robot_cloud", PointCloud, queue_size=1)

listener2 = tf.TransformListener()

scan = LaserScan()


def scan_cb(msg):
    scan = msg

    #print('A')

    start_angle = scan.angle_min
    step_angle  = scan.angle_increment
    last_angle  = scan.angle_max
    #print(last_angle)

    filter_angle = math.radians(0)
    end_angle = start_angle + filter_angle

    current_angle = start_angle

    numOfPoints = 0
    index_array = []

    
    start_idx = 0
    print("")
    while current_angle <= last_angle:
        #numOfPoints = 0
        while current_angle <= end_angle:
            current_angle = current_angle + step_angle
            numOfPoints = numOfPoints + 1
            #print(numOfPoints)

        end_idx = numOfPoints
        ranges = scan.ranges[start_idx:end_idx]
        min_idx = np.argmin(ranges)
        min_idx = min_idx + start_idx
        
        #print(min_idx)

        start_idx = numOfPoints

        end_angle = current_angle + filter_angle

        if scan.ranges[min_idx] > 0.1:
            index_array = np.append(index_array, min_idx)
        
    index_array = np.asarray(index_array, dtype=np.uint16)
    #print(index_array)

    # Transform polar coordinates to cartesian
    cartesian_coordinates = np.zeros((len(index_array), 3))
    #cartesian_coordinates = []

    for idx,i in enumerate(index_array):
        trans_angle = start_angle + i * step_angle

        x = scan.ranges[i] * math.cos(trans_angle)
        y = scan.ranges[i] * math.sin(trans_angle)
        z = 0

        #Test = namedtuple('Test',["x", "y", "z"])
        #test = Test(x=x1, y=y1, z=z1)
        #test2 = list(test)
        #print(test2.x)

        #print(scan.ranges[i])

        #cartesian_coordinates = np.append(cartesian_coordinates, [x, y, z])
        cartesian_coordinates[idx][0] = x
        cartesian_coordinates[idx][1] = y
        cartesian_coordinates[idx][2] = z

    #print(cartesian_coordinates)

    cartesian_cloud = PointCloud()
    cartesian_cloud.header.stamp = rospy.Time.now()
    cartesian_cloud.header.frame_id = 'laser'
    cartesian_cloud.points = cartesian_coordinates

    transformed_cloud = listener2.transformPointCloud('robot',cartesian_cloud)
    #print(transformed_cloud.points)

    
    cleaned_points = []
    # Delete points where x is larger or smaller than our boundries
    for idx,i in enumerate(transformed_cloud.points):
        
        if i.y < -0.20: #or i.y > 0.2:
            #print(i.x)
            cleaned_points = np.append(cleaned_points, idx)
        
        if i.y > 0.20: #or i.y > 0.2:
            #print(i.x)
            cleaned_points = np.append(cleaned_points, idx)

    cleaned_points = cleaned_points.astype(int)
    print(cleaned_points)
    
    transformed_cloud.points = np.delete(transformed_cloud.points, cleaned_points, axis=0)
    

    pc_pub.publish(transformed_cloud)


    '''
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
    '''

        
#rospy.Subscriber("/cloud", PointCloud2, scan_cb, queue_size=1)
rospy.Subscriber("/scan", LaserScan, scan_cb, queue_size=1)
rospy.spin()
