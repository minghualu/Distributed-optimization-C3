import random
import numpy as np
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, pickup, dropoff):
        #self.dropoff = dropoff

        self.stateSpace = [i for i in range(10000) if i not in range(dropoff*100, dropoff*100+99)]
        self.reward = 0

        #self.stateSpace.remove([dropoff*100:dropoff*100+99])

        self.stateSpacePlus = [i for i in range(10000)]
        self.possibleActions = ['Up', 'Down', 'Left', 'Right', 'Stay']
        
        self.Q = {}
        for state in self.stateSpacePlus:
            for action in self.possibleActions:
                self.Q[state, action] = 0

        self.agentPosition = pickup

    def isTerminalState(self, state):
        return state in self.stateSpacePlus and state not in self.stateSpace

    def updatePosition(self, newPos):
        self.agentPosition = newPos

    def getState(self, resultingPos, otherAgentPos):
        return resultingPos*100 + otherAgentPos

    def updateReward(self, reward):
        self.reward = reward

