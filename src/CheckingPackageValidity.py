#!/usr/bin/env python3

import time
from src.EpisodeManager import *

episode = EpisodeManager()
episode.runEpisode()
time.sleep(5)
episode.killSimulation()