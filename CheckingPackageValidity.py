#!/usr/bin/env python3

import time
from EpisodeManager import *

episode = EpisodeManager()
episode.runEpisode()
time.sleep(5)
episode.killSimulation()