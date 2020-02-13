class Agent:
    def __init__(self, pickup, dropoff, n, m):
        # self.dropoff = dropoff
        self.n = n
        self.m = m

        #self.stateSpace = [i for i in range((n*m)**2) if i not in range(dropoff * n*m, dropoff * n*m + n*m)]
        self.terminalState = [i for i in range((n*m)**2) if i in range(dropoff*n*m, dropoff*n*m + n*m)]
        self.reward = 0
        self.posSpace = [i for i in range(n*m)]

        # self.stateSpace.remove([dropoff*100:dropoff*100+99])

        self.stateSpacePlus = [i for i in range((n*m)**2)]
        self.possibleActions = ['Up', 'Down', 'Left', 'Right', 'Stay']

        self.Q = {}
        for state in self.stateSpacePlus:
            for action in self.possibleActions:
                self.Q[state, action] = 0

        self.agentPosition = pickup

    def reset(self, pickup):
        self.reward = 0
        self.agentPosition = pickup

    def isTerminalState(self, state):
        return state in self.terminalState
        #return state in self.stateSpacePlus and state not in self.stateSpace

    def updatePosition(self, newPos):
        self.agentPosition = newPos

    def getState(self, resultingPos, otherAgentPos):
        return resultingPos * self.n*self.m + otherAgentPos

    def updateReward(self, reward):
        self.reward = reward
