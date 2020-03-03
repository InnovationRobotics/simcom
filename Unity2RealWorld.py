import numpy as np
from geometry_msgs.msg import Pose, Point, Quaternion, Vector3


def positionROS2RW(position):
    A = np.array([[0,-1,0,-500], [1,0,0,0], [0,0,1,0], [0,0,0,1]])
    B = np.array([position.x, position.y, position.z, 1])
    RWPos =  A.dot(B)
    RWPos = RWPos[0:3]
    return RWPos


def rotationROS2RW(orientation):
    RWOrient = Quaternion()
    RWOrient.x = -orientation.y - 500
    RWOrient.y = orientation.x
    RWOrient.z = orientation.z
    RWOrient.w = orientation.w
    return RWOrient


def velAccROS2RW(velocity):
    RWVelocity = Vector3()
    RWVelocity.x = -velocity.y
    RWVelocity.y = velocity.x
    RWVelocity.z = velocity.z
    return RWVelocity