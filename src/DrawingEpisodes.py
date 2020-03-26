#!/usr/bin/env python3
#
#    This file includes mainly a class "randomEpisode" that:
#       - draws localization of vehicle
#       - draws number of rocks
#       - draws position of each rock
#       - save in a json file
#    Author: Michele
#    Project: SmartLoader - Innovation

import json
import random
from geometry_msgs.msg import PoseStamped, Quaternion, Vector3
import math
from math import pi as pi
import src.Unity2RealWorld as toRW
import os

def deleteFileIfExists(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")

class randomEpisode:
    actual_seed=0
    data = {}
    data['Objects'] = []
    NumberOfRocks = 0
    VehiclePosition= PoseStamped()

    def __init__(self, typeOfRand, newseed):
        if newseed != 0:
            self.actual_seed = random.seed(None,2)
        if typeOfRand == "verysimple":
            self.NumberOfRocks = random.randint(1,10)
        else:
            self.NumberOfRocks = random.randint(1,10)
        self.VehiclePosition.pose.position.x = random.uniform(0,500)
        self.VehiclePosition.pose.position.y = 0
        self.VehiclePosition.pose.position.z = random.uniform(0,500)
        euler_orient = Vector3()
        euler_orient.x = 0
        euler_orient.y = random.uniform(-pi,pi)
        euler_orient.z = 0 #random.uniform(-pi,pi)
        quat_orient = toRW.euler_to_quaternion(euler_orient.x, euler_orient.y, euler_orient.z)
        self.VehiclePosition.pose.orientation.x = quat_orient[0] #random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.y = quat_orient[1] #random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.z = quat_orient[2] #random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.w = quat_orient[3] #random.uniform(-1,1)
        self.data['Objects'].append({
            'Name': 'BobCat',
            'Id': 'BobCat',
            'Position':
                {
                    'x': self.VehiclePosition.pose.position.x,
                    'y': self.VehiclePosition.pose.position.y,
                    'z': self.VehiclePosition.pose.position.z
                },
            'Rotation':
                {
                    'x': self.VehiclePosition.pose.orientation.x,
                    'y': self.VehiclePosition.pose.orientation.y,
                    'z': self.VehiclePosition.pose.orientation.z,
                    'w': self.VehiclePosition.pose.orientation.w
                },
            'Scale':
                {
                'x': 1,
                'y': 1,
                'z': 1
                 }
        })

        BobcatX = self.VehiclePosition.pose.position.x
        BobcatZ = self.VehiclePosition.pose.position.z
        XMin = BobcatX - 1
        XMax = BobcatX + 1
        ZMin = BobcatZ - 1.5
        ZMax = BobcatZ + 1.5
        for i in range(self.NumberOfRocks):
            id = (i+1).__str__()
            eulerRot = Vector3()
            eulerRot.x = 0
            eulerRot.y = random.uniform(-pi, pi)
            eulerRot.z = 0 #random.uniform(-pi, pi)
            quatRot = toRW.euler_to_quaternion(eulerRot.x, eulerRot.y, eulerRot.z)
            self.data['Objects'].append({
                'Name': 'Rock',
                'Id': id,
                'Position':
                    {
                        "x": random.uniform(XMin,XMax),
                        "y": 0,
                        "z": random.uniform(ZMin,ZMax)
                    },
                "Rotation":
                    {
                        "x": quatRot[0], #random.uniform(-1,1),
                        "y": quatRot[1], #random.uniform(-1,1),
                        "z": quatRot[2], #random.uniform(-1,1),
                        "w": quatRot[3] #random.uniform(-1,1)
                    },
                "Scale":
                    {
                        "x": 0.1,
                        "y": 0.1,
                        "z": 0.1
                    }
            })
        deleteFileIfExists('/home/graphics/ws/interfaces/src/simcom/config/InitialScene.json')
        with open('/home/graphics/ws/interfaces/src/simcom/config/InitialScene.json', 'w') as outfile:
            json.dump(self.data, outfile)

class recorderEpisode:
    actual_seed=0
    data = {}
    data['Objects'] = []
    NumberOfRocks = 0
    VehiclePosition= PoseStamped()

    def __init__(self, newseed):
        if newseed != 0:
            self.actual_seed = random.seed(None,2)

        self.NumberOfRocks = 2

        self.VehiclePosition.pose.position.x = 250
        self.VehiclePosition.pose.position.y = 0
        self.VehiclePosition.pose.position.z = 250
        euler_orient = Vector3()
        euler_orient.x = 0
        euler_orient.y = random.uniform(-pi,pi)
        euler_orient.z = 0 #random.uniform(-pi,pi)
        quat_orient = toRW.euler_to_quaternion(euler_orient.x, euler_orient.y, euler_orient.z)
        self.VehiclePosition.pose.orientation.x = quat_orient[0] #random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.y = quat_orient[1] #random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.z = quat_orient[2] #random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.w = quat_orient[3] #random.uniform(-1,1)
        self.data['Objects'].append({
            'Name': 'BobCat',
            'Id': 'BobCat',
            'Position':
                {
                    'x': self.VehiclePosition.pose.position.x,
                    'y': self.VehiclePosition.pose.position.y,
                    'z': self.VehiclePosition.pose.position.z
                },
            'Rotation':
                {
                    'x': self.VehiclePosition.pose.orientation.x,
                    'y': self.VehiclePosition.pose.orientation.y,
                    'z': self.VehiclePosition.pose.orientation.z,
                    'w': self.VehiclePosition.pose.orientation.w
                },
            'Scale':
                {
                'x': 1,
                'y': 1,
                'z': 1
                 }
        })

        BobcatX = self.VehiclePosition.pose.position.x
        BobcatZ = self.VehiclePosition.pose.position.z
        XMin = BobcatX - 5
        XMax = BobcatX + 5
        ZMin = BobcatZ - 5
        ZMax = BobcatZ + 5

        id = (1).__str__()
        eulerRot = Vector3()
        eulerRot.x = 0
        eulerRot.y = random.uniform(-pi, pi)
        eulerRot.z = 0 #random.uniform(-pi, pi)
        quatRot = toRW.euler_to_quaternion(eulerRot.x, eulerRot.y, eulerRot.z)
        self.data['Objects'].append({
            'Name': 'Rock',
            'Id': id,
            'Position':
                {
                    "x": random.uniform(XMin,XMax),
                    "y": 0,
                    "z": random.uniform(ZMin,ZMax)
                },
            "Rotation":
                {
                    "x": quatRot[0], #random.uniform(-1,1),
                    "y": quatRot[1], #random.uniform(-1,1),
                    "z": quatRot[2], #random.uniform(-1,1),
                    "w": quatRot[3] #random.uniform(-1,1)
                },
            "Scale":
                {
                    "x": 0.3,
                    "y": 0.3,
                    "z": 0.3
                }
        })

        id = (2).__str__()
        eulerRot = Vector3()
        eulerRot.x = 0
        eulerRot.y = random.uniform(-pi, pi)
        eulerRot.z = 0 #random.uniform(-pi, pi)
        quatRot = toRW.euler_to_quaternion(eulerRot.x, eulerRot.y, eulerRot.z)
        self.data['Objects'].append({
            'Name': 'Rock',
            'Id': id,
            'Position':
                {
                    "x": random.uniform(XMin,XMax),
                    "y": 0,
                    "z": random.uniform(ZMin,ZMax)
                },
            "Rotation":
                {
                    "x": quatRot[0], #random.uniform(-1,1),
                    "y": quatRot[1], #random.uniform(-1,1),
                    "z": quatRot[2], #random.uniform(-1,1),
                    "w": quatRot[3] #random.uniform(-1,1)
                },
            "Scale":
                {
                    "x": 0.1,
                    "y": 0.1,
                    "z": 0.1
                }
        })
        with open('/home/graphics/ws/interfaces/src/simcom/config/InitialScene.json', 'w') as outfile:
            json.dump(self.data, outfile)

if __name__ == '__main__':
    for j in range(3):
        scenario = randomEpisode("coucou",j)

