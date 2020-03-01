import numpy as np

class Warehouse:
    def __init__(self, n, m, start1, start2, goal1, goal2):
        self.n = n
        self.m = m
        self.start = [start1, start2]
        self.goal = [goal1, goal2]
        self.grid = np.zeros((n, m))
        self.state = np.zeros((1, n*m))
        self.state[0][start1] = 1
        self.state[0][start2] = 1
        self.agentsPos = [start1, start2]

        self.posSpace = [i for i in range(n*m)]

        # Defining all actions
        self.actionSpace = [-self.m, self.m, -1, 1]
        self.possibleActions = [0, 1, 2, 3] #Up, down, left, right

        # Walls
        #self.walls = [1, 11, 21, 31, 41, 51, 61, 93, 83, 73, 63, 53]
        self.walls = []

    # Translate to x and y coordinates
    def getAgentRowAndColumn(self, agent_nr):
        x = self.agentsPos[agent_nr] // self.m
        y = self.agentsPos[agent_nr] % self.m
        return x, y


    def getWalls(self, wall):
        x = wall // self.m
        y = wall % self.m
        if self.grid[x][y] != 1:
            self.grid[x][y] = 2
        return x, y

    # Prohibits wrong movement
    def offGridMove(self, newPos, oldPos):
        # if we move into a row not in the grid
        if newPos in self.walls:
            return True
        if newPos not in self.posSpace:
            return True
        # if we're trying to wrap around to next row
        elif oldPos % self.m == 0 and newPos % self.m == self.m - 1:
            return True
        elif oldPos % self.m == self.m - 1 and newPos % self.m == 0:
            return True
        else:
            return False
    
    def isTerminalState(self, resultingPos, agent_nr):
        #if self.state[self.goal[agent_nr]] == 1:
        #    return True
        #else:
        #    return False
        if resultingPos == self.goal[agent_nr]:
            return True
        else:
            return False
        
    def updateState(self, currentPos, resultingPos):
        self.state[0][currentPos] = 0
        self.state[0][resultingPos] = 1

    # Defining one step, with rewards
    def step(self, action, agent_nr):
        #x, y = self.getAgentRowAndColumn(agent)

        currentPos = self.agentsPos[agent_nr]
        resultingPos = currentPos + self.actionSpace[action]
        
        if not self.offGridMove(resultingPos, currentPos):
            if not self.isTerminalState(resultingPos, agent_nr):
                if resultingPos in self.walls:
                    reward = -50
                #elif resultingPos == self.agentsPos[agent_nr-1]:
                elif self.state[0][resultingPos] == 1:
                    reward = -100
                    print('collided')
                    return self.state, reward, False, 1
                else:
                    reward = -1
                    #print('stepped')
            else:
                reward = 50
                print('Reached goal', agent_nr)

            #self.setGrid(resultingPos, agent)
            self.updateState(currentPos, resultingPos)
            self.agentsPos[agent_nr] = resultingPos
            return self.state, reward, self.isTerminalState(resultingPos, agent_nr), None
        else:
            reward = -1
            return self.state, reward, self.isTerminalState(currentPos, agent_nr), None

    def reset(self):
        #self.grid = np.zeros((self.n, self.m))
        self.state = np.zeros((1, self.n*self.m))
        self.state[0][self.start[0]] = 1
        self.state[0][self.start[1]] = 1
        self.agentsPos = [self.start[0], self.start[1]]

    # Random action while exploring
    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)
