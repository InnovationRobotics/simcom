# Package simcom: 
#         Communication with simulation

It is built to work with Unity3d simulator.
There are:
1. Two classes: 
    1. randomEpisode that draws the parameters of the episode
    2. EpisodeManager that implements three important methods:
        1. generateAndRunWholeEpisode(): draw and run episode
        2. runEpisode(): run already drawn episode
        3. killSimulation(): power down the simulation
1. Unity2RealWorld: A library of functions for converting coordinates that we received from ROS to Real World.

## Install

1. Install ROS Melodic
2. pip3 install paramiko scp
3. Install pycharm with a launch script
