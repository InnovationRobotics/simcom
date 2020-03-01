#!/usr/bin/env python3
import sys, os, time
import logging
import multiprocessing as mp
from multiprocessing import Process, Queue
from paramiko import SSHClient
from scp import SCPClient
import socket
import json
import random as rnd
from DrawingEpisodes import randomEpisode

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

class EpisodeManager:
    scenario = {}
    scenarioConfigFile = open("InitialScene.json", 'wt')
    sim_host="192.168.100.21"
    sim_port= 22
    scenario_file="/home/sload/InitialScene.json"
    oururl_file = "/home/sload/URLConfig.json"
    destination_scenario="./UnityBuild/smartloader/smartloader_Data/StreamingAssets/InitialScene.json"
    destination_url="./UnityBuild/smartloader/smartloader_Data/StreamingAssets/URLConfig.json"
 #   run_simulation_cmd="./UnityBuild/smartloader/smartloader.exe"
    run_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d c:/users/gameuser/UnityBuild/smartloader/smartloader.exe"
    kill_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 -d taskkill /F /IM smartloader.exe"
    simProcess = 0
    myip = get_ip()
    myurl= ""


    def generateNewSerieScenario(self, new_seed):
    #    new_seed=rnd.seed(None,2)
        print("start a new serie of scenarios:"+new_seed.__str__())
        randomEpisode(new_seed)


    def generateNewScenario(self):
        print("generate new scenario")
        randomEpisode(0)


    def ssh_scp_files(self, ssh_host, ssh_user, ssh_password, ssh_port, source_volume, destination_volume):
        logging.info("In ssh_scp_files()method, to copy the files to the server")
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(ssh_host, ssh_port, ssh_user, ssh_password)
       # ssh.connect(ssh_host, ssh_user, ssh_password, look_for_keys=False)
        scp = SCPClient(ssh.get_transport())
        scp.put(source_volume, destination_volume)
#        with SCPClient(ssh.get_transport()) as scp:
#            scp.put(source_volume, recursive=True, remote_path=destination_volume)

    def scpScenarioToSimulation(self):
        print("scp to simulation")
 #       self.ssh_scp_files(self.this_host,"gameuser","PlayMe1", self.this_port, "/home/sload/InitialScene.json", "AAAAA.json")
        self.ssh_scp_files(self.sim_host,"gameuser","PlayMe1", self.sim_port, self.scenario_file, self.destination_scenario)
        self.ssh_scp_files(self.sim_host,"gameuser","PlayMe1", self.sim_port, self.oururl_file, self.destination_url)

    def runSimulation(self):
        print("Run Simulation")
        p = SSHClient()
        #p.set_missing_host_key_policy(
        #    paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
        p.load_system_host_keys()
        p.connect(self.sim_host, self.sim_port, "gameuser","PlayMe1")
        stdin, stdout, stderr = p.exec_command(self.run_simulation_cmd)
        opt = stdout.readlines()
        opt = "".join(opt)
        print(opt)

    def killSimulation(self):
        print("Kill Simulation")
        time.sleep(5)
        p = SSHClient()
        #p.set_missing_host_key_policy(
        #    paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
        p.load_system_host_keys()
        p.connect(self.sim_host, self.sim_port, "gameuser","PlayMe1")
        stdin, stdout, stderr = p.exec_command(self.kill_simulation_cmd)
        opt = stdout.readlines()
        opt = "".join(opt)
        print(opt)
        self.simProcess.terminate()
        self.simProcess.join()
        self.simProcess = 0

    def runEpisode(self):
        if self.simProcess != 0:
            print("Simulation is already running... wait few minutes and try again")
            return
       # self.scpScenarioToSimulation()
        self.simProcess = mp.Process(target=self.runSimulation())
        self.simProcess.start()

    def __init__(self):
        # Get the IP address of this machine and throw it in the URLConfig.json file
        self.myip = get_ip()
        self.myurl = "ws://"+self.myip.__str__()+":9090"
        print(self.myurl)
        data = {}
        data['URL'] = self.myurl
        #data['URL'].append(self.myurl)
        with open(self.oururl_file, 'w') as outfile:
            json.dump(data, outfile)

if __name__ == '__main__':
    episode = EpisodeManager()
    #episode.ScpScenarioToSimulation()
    mp.set_start_method('fork')
    episode.runEpisode()
#    sometimerproc = mp.Process(target=episode.killSimulation())
#    print("I am after calling to kill")

#    episode.simProcess = mp.Process(target=episode.runSimulation())
#    sometimerproc.start()
    print("I am before start")

#    episode.simProcess.start()
    print("I am here")
    time.sleep(5)
    print("I am here-here")
    episode.killSimulation()
    print("I am here-here-here")