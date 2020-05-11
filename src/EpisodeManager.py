#!/usr/bin/env python3
#
#    This file includes mainly a class "EpisodeManager" and some utility function called get_ip
#    Author: Michele
#    Project: SmartLoader - Innovation
#
#  For now, hard coded:
#   sim_host="192.168.100.21"
#     sim_port= 22
#     scenario_file="/home/sload/InitialScene.json"
#     oururl_file = "/home/sload/URLConfig.json"
#     destination_scenario="./UnityBuild/smartloader/smartloader_Data/StreamingAssets/InitialScene.json"
#     destination_url="./UnityBuild/smartloader/smartloader_Data/StreamingAssets/URLConfig.json"
#  #   run_simulation_cmd="./UnityBuild/smartloader/smartloader.exe"
#     run_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d c:/users/gameuser/UnityBuild/smartloader/smartloader.exe"
#     kill_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d taskkill /F /IM smartloader.exe"

import sys, os, time
import os.path
import re
from shutil import copyfile
import logging
import multiprocessing as mp
from multiprocessing import Process, Queue
from paramiko import SSHClient, AuthenticationException, SSHException, BadHostKeyException
from scp import SCPClient
import socket
import json
from src.DrawingEpisodes import randomEpisode, MultipleRocksEpisode, loaderEpisode
from src.DrawingEpisodes import determinePathToConfig

### The goal of this function is to determine the IP address of the computer running this module.
### Knowing the IP address will allow to configure the URLConfig.json for the simulation without human intervention
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



#  The class EpisodeManager deals with everything that has to do with an episode for training an agent with RL.
#  It is compliant with gym methodology.
#  What should be called:
#       episode = EpisodeManager()
#       episode.generateAndRunWholeEpisode()
#       episode.killSimulation()
# Note that if you want to run the same episode each time, you should call:
#       episode.runEpisode()
#
#
class EpisodeManager:
    local = False
    scenario = {}
    scenarioConfigFile = open("InitialScene.json", 'wt')
    sim_host="192.168.100.21"
    sim_port= 22
    simProcess = 0
    myip = get_ip()
    myurl= ""


    def generateNewSerieScenario(self, new_seed):
    #    new_seed=rnd.seed(None,2)
        print("start a new serie of scenarios:"+new_seed.__str__())
        randomEpisode(new_seed)


    def generateNewScenario(self,typeOfRand, numstones, marker):
        print("generate new scenario")
        path = determinePathToConfig()

        if typeOfRand == "verybasic":
            file = path +"/VeryBasicInitialScene.json"
            copyfile(file,"InitialScene.json")
        elif typeOfRand == "MultipleRocks":
            MultipleRocksEpisode(0, numstones, marker)
        elif typeOfRand == "AlgxVeryBasic":
            file = path + "/AlgxInitialScene.json"
            copyfile(file, path+"/InitialScene.json")
        elif typeOfRand == "AlgxBasic":
            loaderEpisode(0)
        else:
            randomEpisode(typeOfRand, 0)

# This method secure copies a file  to a remote computer
    def ssh_scp_file(self, ssh_host, ssh_user, ssh_password, ssh_port, source_volume, destination_volume):
        logging.info("In ssh_scp_files()method, to copy the files to the server")
        if (self.local):
            command = "cp " + source_volume + " " + destination_volume
        else:
            command = "sshpass -p " + ssh_password + " scp "+ source_volume+" " + ssh_user +"@"+ssh_host+":"+destination_volume

        print(command)
        os.system(command)



# This method encapsulates ssh_scp_files and copies all the files needed via secure cp to the computer that runs Unity
    def scpScenarioToSimulation(self):
        print("scp to simulation")
 #       self.ssh_scp_files(self.this_host,"gameuser","PlayMe1", self.this_port, "/home/sload/InitialScene.json", "AAAAA.json")
        self.ssh_scp_file(self.sim_host,"gameuser","PlayMe1", self.sim_port, self.scenario_file, self.destination_scenario)
        self.ssh_scp_file(self.sim_host,"gameuser","PlayMe1", self.sim_port, self.oururl_file, self.destination_url)
        self.ssh_scp_file(self.sim_host,"gameuser","PlayMe1", self.sim_port, self.velodyne_file, self.destination_velo)

    def runSimulation(self):
        print("Run Simulation Brutal Force")
        if (self.local):
            command = self.run_simulation_cmd
        else:
            command = "sshpass -p PlayMe1 ssh "+self.sim_host+" -l gameuser "+ self.run_simulation_cmd
            #command = "sshpass -p PlayMe1 ssh 192.168.100.21 -l gameuser "+ self.run_simulation_cmd
        print(command)
        os.system(command)


    def killSimulation(self):
        print("Kill Simulation Brutal Force")
        if (self.local):
            command = self.kill_simulation_cmd
        else:
            command = "sshpass -p PlayMe1 ssh "+self.sim_host+" -l gameuser "+ self.kill_simulation_cmd
 #       command = "sshpass -p PlayMe1 ssh 192.168.100.21 -l gameuser "+ self.kill_simulation_cmd
        print(command)
        os.system(command)

    def runEpisode(self):
        if self.simProcess != 0:
            print("Simulation is already running... wait few minutes and try again")
            return
       # self.scpScenarioToSimulation()
        try:
            self.simProcess = mp.Process(target=self.runSimulation())
            self.simProcess.start()
        except:
            time.sleep(1)
         #   self.generateAndRunWholeEpisode("verybasic")


    def generateAndRunWholeEpisode(self, typeOfRand="verybasic", numstones="1", marker=False):
        if self.simProcess != 0:
            print("Simulation is already running... wait few minutes and try again")
            return
        self.generateNewScenario(typeOfRand, int(numstones), marker)
        try:
            self.scpScenarioToSimulation()
        except:
            time.sleep(1)
            print("Stopped this scenario: try runEpisode")
            raise #("Banner")
        else:
            try:
                self.simProcess = mp.Process(target=self.runSimulation())
                self.simProcess.start()
            except:
                time.sleep(1)
                print("Stopped this scenario here")
                raise #("Banner")

    def FillDefault(self):
        self.scenario_file="/home/sload/InitialScene.json"
        self.oururl_file = "/home/sload/URLConfig.json"
        self.destination_scenario="./UnityBuilds/sl_0405/smartloader_Data/StreamingAssets/InitialScene.json"
        self.destination_url="./UnityBuilds/sl_0405/smartloader_Data/StreamingAssets/URLConfig.json"
        self.destination_velo="./UnityBuilds/sl_0405/smartloader_Data/StreamingAssets/Velodyne.json"
        self.run_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d c:/users/gameuser/UnityBuilds/sl_0405/activateme.cmd"
        self.kill_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d taskkill /F /IM smartloader.exe"

    def __init__(self):
        # Where are we

        tlocal = determinePathToConfig()
        print(tlocal)

        if tlocal == None:
            self.FillDefault()
        else:
            conFile = tlocal+"//config.json"
            if (not os.path.exists(conFile)):
                self.FillDefault()
            else:
                with open(conFile) as json_file:
                    data = json.load(json_file)

                    self.sim_host = data['sim_host']
                    if (self.sim_host == "127.0.0.1"):
                        self.local = True
                    else:
                        self.local = False
                    self.sim_port = data['sim_port']
                    self.scenario_file = tlocal+"//"+data['scenario_file']
                    self.oururl_file = tlocal+"//"+data['oururl_file']
                    self.velodyne_file = tlocal+"//Velodyne.json"

                    self.sim_root = os.getenv('HOME') + '//' + data['sim_root']
                    if self.local == True:
                        self.destination_scenario = self.sim_root + "//" + data['destination_scenario']
                        self.destination_url = self.sim_root + "//" +data['destination_url']
                        self.destination_velo = self.sim_root + "//" + data['destination_velo']
                        self.run_simulation_cmd = self.sim_root + "//" + data['run_simulation_cmd']
                    else:
                        self.destination_scenario = data['destination_scenario']
                        self.destination_url = data['destination_url']
                        self.destination_velo = data['destination_velo']
                        self.run_simulation_cmd=data['run_simulation_cmd']
                    self.kill_simulation_cmd = data['kill_simulation_cmd']
        #else: works with default
            #
        # Get the IP address of this machine and throw it in the URLConfig.json file
        self.myip = get_ip()
        self.myurl = "ws://"+self.myip.__str__()+":9090"
        print(self.myurl)
        data2 = {}
        data2['URL'] = self.myurl
        data2['ConnectToRos'] = "true"
        #data['URL'].append(self.myurl)
        with open(self.oururl_file, 'w') as outfile:
            json.dump(data2, outfile, indent=4)

        with open(self.velodyne_file) as json_file:
            velodata = json.load(json_file)
        velodata["Ip"]=self.myip.__str__()

        with open(self.velodyne_file, 'w') as outvelo:
            json.dump(velodata, outvelo, indent=4)

if __name__ == '__main__':
    episode = EpisodeManager()
    #episode.ScpScenarioToSimulation()
    mp.set_start_method('fork')
#    episode.generateAndRunWholeEpisode()
    episode.generateAndRunWholeEpisode("AlgxVeryBasic")
#    episode.generateAndRunWholeEpisode("MultipleRocks", 12)
#    episode.generateAndRunWholeEpisode("other")

    print("I am here:"+time.clock().__str__())
    time.sleep(60)
    print("I am here-here:"+time.clock().__str__())
    episode.killSimulation()
    print("I am here-here-here:"+time.clock().__str__())