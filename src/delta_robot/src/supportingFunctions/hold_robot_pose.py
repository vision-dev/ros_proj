#!/usr/bin/env python3


'''
	Matic Vodopivec
	5.7.2022

	Help:
	Hold robot still relative to the ground (robot compensating tracks velocity)



'''


import rospy


import numpy as np

def hold_robot_poz(current_poz, linear_velocity, dt):
    '''
    Inputs:
        - current_poz -> Current robot position (np.array of lenght 5)
        - linear_velocity -> Linear velocity of track robot
        - dt -> Cycle time
    Outputs:
        - New points of delta robot
    '''
    new_poz = current_poz

    points_X = current_poz[1]

    points_X = points_X + linear_velocity * dt

    new_poz[1] = points_X

    return new_poz

