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
from src.DrawingEpisodes import randomEpisode
from src.DrawingEpisodes import recorderEpisode, recorderEpisode_mr
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
    scenario_file="/home/sload/InitialScene.json"
    oururl_file = "/home/sload/URLConfig.json"
    destination_scenario="./UnityBuilds/smartloader28/smartloader_Data/StreamingAssets/InitialScene.json"
    destination_url="./UnityBuilds/smartloader28/smartloader_Data/StreamingAssets/URLConfig.json"
#    run_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d pwd"
    run_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d c:/users/gameuser/smartloader.exe"

 #   run_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d c:/users/gameuser/UnityBuilds/smartloader28/smartloader.exe"
    kill_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d taskkill /F /IM smartloader.exe"
    simProcess = 0
    myip = get_ip()
    myurl= ""


    def generateNewSerieScenario(self, new_seed):
    #    new_seed=rnd.seed(None,2)
        print("start a new serie of scenarios:"+new_seed.__str__())
        randomEpisode(new_seed)


    def generateNewScenario(self,typeOfRand):
        print("generate new scenario")
        if typeOfRand == "verybasic":
            path = os.getcwd()
            file = path +"/VeryBasicInitialScene.json"
            copyfile(file,"InitialScene.json")
        elif typeOfRand == "recorder":
            recorderEpisode(0)

        elif typeOfRand == "recorder_mr":
            recorderEpisode_mr(0)
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


    def generateAndRunWholeEpisode(self, typeOfRand):
        if self.simProcess != 0:
            print("Simulation is already running... wait few minutes and try again")
            return
        self.generateNewScenario(typeOfRand)
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

    def __init__(self):
        # Where are we
        mydic = sys.path
        mypath = ""
        for i in mydic:
            if (i.find("simcom")!=-1):
                mypath = i
                break
        if mypath != "":
            tlocal = mypath
        else:
            tlocal = os.getcwd()

        print(tlocal)
        local = re.sub('/src$', '', tlocal)
        configDir = local +"//config"
        os.chdir(configDir)
        local = os.getcwd()
        confFile = configDir+"//config.json"

        if (os.path.exists(confFile)):
             with open(confFile) as json_file:
                data = json.load(json_file)

                self.sim_host = data['sim_host']
                if (self.sim_host == "127.0.0.1"):
                    self.local = True
                else:
                    self.local = False
                self.sim_port = data['sim_port']
                self.scenario_file = configDir+"//"+data['scenario_file']
                self.oururl_file = configDir+"//"+data['oururl_file']
                self.sim_root = os.getenv('HOME') + '//' + data['sim_root']
                if self.local == True:
                    self.destination_scenario = self.sim_root + "//" + data['destination_scenario']
                    self.destination_url = self.sim_root + "//" +data['destination_url']
                    self.run_simulation_cmd = self.sim_root + "//" + data['run_simulation_cmd']
                else:
                    self.destination_scenario = data['destination_scenario']
                    self.destination_url = data['destination_url']
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
        #data['URL'].append(self.myurl)
        with open(self.oururl_file, 'w') as outfile:
            json.dump(data2, outfile)

if __name__ == '__main__':
    episode = EpisodeManager()
    #episode.ScpScenarioToSimulation()
    mp.set_start_method('fork')
    episode.generateAndRunWholeEpisode("recorder")
#    sometimerproc = mp.Process(target=episode.killSimulation())
#    print("I am after calling to kill")

#    episode.simProcess = mp.Process(target=episode.runSimulation())
#    sometimerproc.start()
    print("I am before start")

#    episode.simProcess.start()
    print("I am here")
    time.sleep(60)
    print("I am here-here")
    episode.killSimulation()
    print("I am here-here-here")