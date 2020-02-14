class Agent:
    def __init__(self, pickup, dropoff, n, m):
        self.dropoff = dropoff
        self.pickup = pickup
        self.n = n
        self.m = m

        self.reward = 0
        self.posSpace = [i for i in range(n*m)]
        self.possibleActions = ['Up', 'Down', 'Left', 'Right', 'Stay']

        self.Q = {}
        for i in range((n*m)**2):
            for action in self.possibleActions:
                self.Q[i, action] = 0

        self.agentPosition = pickup

    def reset(self, pickup):
        self.reward = 0
        self.agentPosition = pickup

    def isTerminalState(self, resultingPos):
        if resultingPos == self.dropoff:
            return True
        else:
            return False

    def updatePosition(self, newPos):
        self.agentPosition = newPos

    def getState(self, resultingPos, otherAgentPos):
        return resultingPos * self.n*self.m + otherAgentPos

    def updateReward(self, reward):
        self.reward = reward

