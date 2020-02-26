#!/usr/bin/env python3
import sys, os
import logging
from paramiko import SSHClient
from scp import SCPClient

class EpisodeManager:
    scenario = {}
    scenarioConfigFile = open("InitialScene.json", 'wt')
    this_host="192.168.100.21"
    this_port= 22
    source_file="/home/sload/InitialScene.json"
    destination_file="./UnityBuild/smartloader/smartloader_Data/StreamingAssets/InitialScene3.json"
 #   run_simulation_cmd="./UnityBuild/smartloader/smartloader.exe"
    run_simulation_cmd="c:/Pstools/psexec /accepteula -i 1 c:/users/gameuser/UnityBuild/smartloader/smartloader.exe"

    def GenerateNewSerieScenario(self, seed):
        print("start a new serie of scenarios")

    def GenerateNewScenario(self, seed):
        print("generate new scenario")

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

    def ScpScenarioToSimulation(self):
        print("scp to simulation")
 #       self.ssh_scp_files(self.this_host,"gameuser","PlayMe1", self.this_port, "/home/sload/InitialScene.json", "AAAAA.json")
        self.ssh_scp_files(self.this_host,"gameuser","PlayMe1", self.this_port, self.source_file, self.destination_file)

    def RunSimulation(self):
        print("Run Simulation")
        p = SSHClient()
        #p.set_missing_host_key_policy(
        #    paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
        p.load_system_host_keys()
        p.connect(self.this_host, self.this_port, "gameuser","PlayMe1")
        stdin, stdout, stderr = p.exec_command(self.run_simulation_cmd)
        opt = stdout.readlines()
        opt = "".join(opt)
        print(opt)


if __name__ == '__main__':
    episode = EpisodeManager()
    #episode.ScpScenarioToSimulation()
    episode.RunSimulation()