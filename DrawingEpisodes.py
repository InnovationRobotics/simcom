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
from geometry_msgs.msg import PoseStamped

class randomEpisode:
    actual_seed=0

    data = {}
    data['Objects'] = []
    NumberOfRocks = 0
    VehiclePosition= PoseStamped()

    def __init__(self, newseed):
        if newseed != 0:
            self.actual_seed = random.seed(None,2)
        self.NumberOfRocks = random.randint(1,10)
        self.VehiclePosition.pose.position.x = random.uniform(0,500)
        self.VehiclePosition.pose.position.y = 0
        self.VehiclePosition.pose.position.z = random.uniform(0,500)
        self.VehiclePosition.pose.orientation.x = random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.y = random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.z = random.uniform(-1,1)
        self.VehiclePosition.pose.orientation.w = random.uniform(-1,1)
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
        for i in range(self.NumberOfRocks):
            id = (i+1).__str__()
            self.data['Objects'].append({
                'Name': 'Rock',
                'Id': id,
                'Position':
                    {
                        "x": random.uniform(0,500),
                        "y": 0,
                        "z": random.uniform(0,500)
                    },
                "Rotation":
                    {
                        "x": random.uniform(-1,1),
                        "y": random.uniform(-1,1),
                        "z": random.uniform(-1,1),
                        "w": random.uniform(-1,1)
                    },
                "Scale":
                    {
                        "x": 0.1,
                        "y": 0.1,
                        "z": 0.1
                    }
            })
        with open('/home/sload/InitialScene.json', 'w') as outfile:
            json.dump(self.data, outfile)

if __name__ == '__main__':
    scenario = randomEpisode(1)

