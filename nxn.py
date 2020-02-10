import gym
import random
import numpy as np
import matplotlib.pyplot as plt


class Warehouse(object):
    #Initializing a n x m grid, currently only working for n = m
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = np.zeros((n, m))
        self.stateSpace = [i for i in range(self.n*self.m*2)]

        #Used for terminal state
        self.stateSpace.remove(self.n*self.m*2-1)
        self.stateSpacePlus = [i for i in range(self.n*self.m*2)]

        #Defining all actions
        self.actionSpace = {'Up': -self.m, 'Down': self.m, 'Left': -1, 'Right': 1, 'Pickup': -(self.m*self.n), 'Drop': self.m*self.n}
        self.possibleActions = ['Up', 'Down', 'Left', 'Right', 'Pickup', 'Drop']
        #self.addPickup(pickup)
        #self.addDropoff(dropoff)
        #self.addBlockade(blockade)
        #self.agentPosition = [random.randint(0, self.n - 1), random.randint(0, self.m - 1)]

        #Start position: first square without item
        self.agentPosition = self.m*self.n
        #Lägg in koordinater som indata
        #self.pickup = pickup
        #self.dropoff = dropoff
        #self.blockade = blockade

    # Defining end of episode
    def isTerminalState(self, state):
        return state in self.stateSpacePlus and state not in self.stateSpace

    # Translate to x and y coordinates
    def getAgentRowAndColumn(self):
        if self.agentPosition < self.m*self.n:
            x = self.agentPosition // self.m
            y = self.agentPosition % self.m
        else:
            x = (self.agentPosition - self.m*self.n) // self.m
            y = (self.agentPosition - self.n*self.m) % self.m
        return x, y

    # Sets old position to new
    def setState(self, state):
        x, y = self.getAgentRowAndColumn()
        self.grid[x][y] = 0
        self.agentPosition = state
        x, y = self.getAgentRowAndColumn()
        self.grid[x][y] = 1

    # Prohibits wrong movement
    def offGridMove(self, newState, oldState):
        s = self.m*self.n
        if newState not in self.stateSpacePlus:
            return True
        elif newState > s-1 and oldState < s or newState < s and oldState > s-1:
            if abs(oldState - newState) == self.m or abs(oldState - newState) == 1:
                return True
        elif oldState % self.m == 0 and newState % self.m == self.m - 1:
            return True
        elif oldState % self.m == self.m - 1 and newState % self.m == 0:
            return True
        else:
            return False

    # Defining one step, with rewards
    def step(self, action):
        x, y = self.getAgentRowAndColumn()
        resultingState = self.agentPosition + self.actionSpace[action]
        #print(self.agentPosition)
        #print(action)

        reward = 0

        if action == 'Up' or action == 'Down' or action == 'Left' or action == 'Right':
            reward = -1
            #print('e')
        elif action == 'Pickup':
            if self.agentPosition == self.m*self.n:
                reward = 5
                #print('a')
            else:
                reward = -10
                #print('b')
        elif action == 'Drop':
            if self.isTerminalState(resultingState):
                #print('c')
                reward = 20
            else:
                reward = -50
                #print('d')

        if not self.offGridMove(resultingState, self.agentPosition):
            self.setState(resultingState)
            return resultingState, reward, self.isTerminalState(self.agentPosition), None
        else:
            return self.agentPosition, reward, self.isTerminalState(self.agentPosition), None

    def reset(self):
        self.agentPosition = self.m*self.n
        self.grid = np.zeros((self.n, self.m))
        return self.agentPosition

    def render(self):
        print('------------------')
        for row in self.grid:
            for col in row:
                if col == 0:
                    print('-', end='\t')
                elif col == 1:
                    # Agent without item
                    if self.agentPosition > self.m*self.n-1:
                        print('X', end='\t')
                    # Agent with item
                    elif self.agentPosition < self.m*self.n:
                        print('O', end='\t')
            print('\n')
        print('------------------')

    # Random action while exploring
    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)


def maxAction(Q, state, actions):
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return actions[action]


if __name__ == '__main__':
    env = Warehouse(3, 7)

    ALPHA = 0.1
    GAMMA = 1.0
    EPSILON = 0.1

    Q = {}
    for state in env.stateSpacePlus:
        for action in env.possibleActions:
            Q[state, action] = 0

    numGames = 50000
    totalRewards = np.zeros(numGames)
    #env.render()

    for i in range(numGames):
        if i % 500 == 0:
            print('starting game', i)

            done = False
            epRewards = 0
            observation = env.reset()
            if i == numGames - 500:
                #Always starts without an item
                env.grid[0][0] = 1
                env.render()

            while not done:
                rand = np.random.random()
                action = maxAction(Q, observation, env.possibleActions) if rand < (1-EPSILON) else env.actionSpaceSample()
                observation_, reward, done, info = env.step(action)
                epRewards += reward

                action_ = maxAction(Q, observation_, env.possibleActions)
                Q[observation, action] = Q[observation, action] + ALPHA*(reward + GAMMA*Q[observation_, action_] - Q[observation, action])
                observation = observation_

                #Explore or exploit
                if EPSILON - 2 / numGames > 0:
                    EPSILON -= 2 / numGames
                else:
                    EPSILON = 0
                totalRewards[i] = epRewards

                # Renders the last episode
                if i == numGames - 500:
                    env.render()
    plt.plot(totalRewards)
    plt.show()

