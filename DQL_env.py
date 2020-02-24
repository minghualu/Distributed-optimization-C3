import numpy as np


class Warehouse:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = np.zeros((n, m))
        self.stateSpace = [i for i in range(self.n*self.m)]

        # Used for terminal state
        self.stateSpace.remove(self.m*self.n-1)
        self.stateSpacePlus = [i for i in range(self.n*self.m)]

        # Defining all actions
        self.actionSpace = [-self.m, self.m, -1, 1]
        self.possibleActions = [0, 1, 2, 3] #Up, down, left, right

        # Start position: first square without item
        self.agentPosition = 0

        # Walls
        self.walls = [1, 11, 21, 31, 41, 51, 61, 94, 74, 64, 54,44,34,24,75,76,77,87,97]

    # Defining end of episode
    def isTerminalState(self, state):
        return state in self.stateSpacePlus and state not in self.stateSpace

    # Translate to x and y coordinates
    def getAgentRowAndColumn(self):
        x = self.agentPosition // self.m
        y = self.agentPosition % self.m
        return x, y

    #Sets old position to new
    def setState(self, state):
        x, y = self.getAgentRowAndColumn()
        self.grid[x][y] = 0
        self.agentPosition = state
        x, y = self.getAgentRowAndColumn()
        self.grid[x][y] = 1

    def getWalls(self, wall):
        x = wall // self.m
        y = wall % self.m
        if self.grid[x][y] != 1:
            self.grid[x][y] = 2
        return x, y

    # Prohibits wrong movement
    def offGridMove(self, newState, oldState):
        # if we move into a row not in the grid
        if newState in self.walls:
            return True
        if newState not in self.stateSpacePlus:
            return True
        # if we're trying to wrap around to next row
        elif oldState % self.m == 0 and newState % self.m == self.m - 1:
            return True
        elif oldState % self.m == self.m - 1 and newState % self.m == 0:
            return True
        else:
            return False

    # Defining one step, with rewards
    def step(self, action):
        x, y = self.getAgentRowAndColumn()
        print(action)
        resultingState = self.agentPosition + self.actionSpace[action]
        #print(self.agentPosition)
        #print(action)

        if not self.isTerminalState(resultingState):
            if resultingState in self.walls:
                reward = -50
            else:
                reward = -1
        else:
            reward = 50

        if not self.offGridMove(resultingState, self.agentPosition):
            self.setState(resultingState)
            return [resultingState], reward, self.isTerminalState(self.agentPosition), None
        else:
            return [self.agentPosition], reward, self.isTerminalState(self.agentPosition), None

    def reset(self):
        self.agentPosition = 0
        self.grid = np.zeros((self.n, self.m))
        return self.agentPosition

    def render(self):
        print('------------------')
        for row in self.grid:
            for col in row:
                if col == 0:
                    print('-', end='\t')
                elif col == 1:
                    print('O', end='\t')
                elif col == 2:
                    print('X', end='\t')
            print('\n')
        print('------------------')

    # Random action while exploring
    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)

