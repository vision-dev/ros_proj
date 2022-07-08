#!/usr/bin/env python3


'''
	Matic Vodopivec
	8.7.2022

	Help:
	Read data from sick scanner LMS111

'''

import sensor_msgs.point_cloud2 as pc2
import rospy
from sensor_msgs.msg import PointCloud2, LaserScan
import laser_geometry.laser_geometry as lg
import math
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud

rospy.init_node("laserscan_to_pointcloud")

lp = lg.LaserProjection()
#pc2_msg = PointCloud2()

pc_pub = rospy.Publisher("converted_pc", PointCloud2, queue_size=1)

def scan_cb(msg):
    # convert the message of type LaserScan to a PointCloud2
    #pc2_msg = lp.projectLaser(msg)
    pc2_msg = msg
    #pc2_msg.header.frame_id = 'world'

    # now we can do something with the PointCloud2 for example:
    # publish it
    pc_pub.publish(pc2_msg)
    
    # convert it to a generator of the individual points
    point_generator = pc2.read_points(pc2_msg)
    print(point_generator)

    # we can access a generator in a loop
    sum = 0.0
    num = 0
    for point in point_generator:
        if not math.isnan(point[2]):
            sum += point[2]
            num += 1
    # we can calculate the average z value for example
    print(str(sum/num))

    # or a list of the individual points which is less efficient
    point_list = pc2.read_points_list(pc2_msg)
    print(point_list)
    

    # we can access the point list with an index, each element is a namedtuple
    # we can access the elements by name, the generator does not yield namedtuples!
    # if we convert it to a list and back this possibility is lost
    #print(point_list[len(point_list)/2].x)

    # definicija listener
    tfBuffer = tf2_ros.Buffer() # buffer 10 sekund
    listener = tf2_ros.TransformListener(tfBuffer)

    pc_world = tfBuffer.transformPoint 
    listener.transformPoint()
    ('world', pc2_msg)
    print(pc_world)

    #trans = tfBuffer.lookup_transform('laser', 'world', rospy.Time(0))
    #print(trans.transform)

        
    



rospy.Subscriber("/cloud", PointCloud2, scan_cb, queue_size=1)
rospy.spin()
