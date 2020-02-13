import numpy as np

class Warehouse:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = np.zeros((n, m))

        # Defining all actions
        self.actionSpace = {'Up': -self.m, 'Down': self.m, 'Left': -1, 'Right': 1, 'Stay': 0}
        self.possibleActions = ['Up', 'Down', 'Left', 'Right', 'Stay']

        # Walls
        # self.walls = [1, 11, 21, 31, 41, 51, 61, 93, 83, 73, 63, 53]
        self.walls = []

    # Translate to x and y coordinates
    def getAgentRowAndColumn(self, agent):
        x = agent.agentPosition // self.m
        y = agent.agentPosition % self.m
        return x, y

    def getWalls(self, wall):
        x = wall // self.m
        y = wall % self.m
        if self.grid[x][y] != 1:
            self.grid[x][y] = 2
        return x, y

    # Prohibits wrong movement
    def offGridMove(self, newPos, oldPos, agent):
        # if we move into a row not in the grid
        if newPos in self.walls:
            return True
        if newPos not in agent.posSpace:
            return True
        # if we're trying to wrap around to next row
        elif oldPos % self.m == 0 and newPos % self.m == self.m - 1:
            return True
        elif oldPos % self.m == self.m - 1 and newPos % self.m == 0:
            return True
        else:
            return False

    # Defining one step, with rewards
    def step(self, action, agent, otherAgentPos):

        currentState = agent.getState(agent.agentPosition, otherAgentPos)
        resultingPos = agent.agentPosition + self.actionSpace[action]
        resultingState = agent.getState(resultingPos, otherAgentPos)

        if agent.agentPosition == otherAgentPos:
            reward = -100
            return currentState, reward, True, 2

        if not self.offGridMove(resultingPos, agent.agentPosition, agent):
            # print(self.agentPosition)
            # print(action)
            #reward = 0
            if not agent.isTerminalState(resultingState):
                if resultingPos in self.walls:
                    reward = -50
                    # agent.updateReward(-50)
                elif otherAgentPos == resultingPos:
                    reward = -100
                    # info = 1 ends episode
                    return resultingState, reward, True, 1
                else:
                    reward = -1
            else:
                reward = 50

            agent.updatePosition(resultingPos)
            agent.updateReward(reward)
            return resultingState, agent.reward, agent.isTerminalState(resultingState), None
        else:
            reward = -1
            agent.updateReward(reward)
            return currentState, agent.reward, agent.isTerminalState(currentState), None

    # Random action while exploring
    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)
