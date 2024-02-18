import pygame
import sys
from Cell import Cell, FireStatus
import random
from UAV import UAV
from typing import List
from pygame.constants import K_a, K_d, K_s, K_w
from ple import PLE 
from ple.games.base.pygamewrapper import PyGameWrapper
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
import deer.experiment.base_controllers as bc
from firefighter import Firefighter


game = Firefighter()
p = PLE(game, fps=60, display_screen=True)
   
qnetwork = MyQNetwork(environment=p)
agent = NeuralAgent(p,qnetwork)
agent.attach(bc.VerboseController())
agent.attach(bc.TranerController())
agent.attach(bc.InterleavedTestEpochController(epoch_length=500, controllers_to_disable=[0,1]))
agent.run(n_epochs=10,epoch_lenth=1000)