#!/usr/bin/env python3
import json
from geometry_msgs.msg import PoseStamped

data = {}
data['objscts'] = []
NumberOfRocks = 2
VehiclePosition= new PoseStamped()
for i in range(NumberOfRocks):
    #Draw Rock position


data = {}
data['objects'] = []
data['objects'].append({
    'name': 'BobCat',
    'Id': 'BobCat',
    'Position':
        {
            'x': 277,
            'y': 0,
            'z': 130
        },
    'Rotation':
        {
            'x':0,
            'y': 0,
            'z': 0.0,
            'w': 0
        },
    'Scale':
        {
            'x': 1,
            'y': 1,
            'z': 1
        }
 })

data['objects'].append({
    'name': 'Rock',
    'Id': '1',
    'Position':
        {
            "x": 277,
            "y": 9,
            "z": 135
        },
    "Rotation":
        {
            "x": 10,
            "y": 0.0,
            "z": 0.0,
            "w": 5
        },
    "Scale":
        {
            "x": 0.1,
            "y": 0.1,
            "z": 0.1
        }
})


with open('InitialScene.json', 'w') as outfile:
    json.dump(data, outfile)

