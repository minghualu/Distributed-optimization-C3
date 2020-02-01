import gym
import random
import numpy as np
import matplotlib.pyplot as plt


class Agent:
    def __init__(self, pickup, dropoff, n, m):
        # self.dropoff = dropoff
        self.n = n
        self.m = m

        self.stateSpace = [i for i in range((n*m)**2) if i not in range(dropoff * n*m, dropoff * n*m + n*m)]
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
        return state in self.stateSpacePlus and state not in self.stateSpace

    def updatePosition(self, newPos):
        self.agentPosition = newPos

    def getState(self, resultingPos, otherAgentPos):
        return resultingPos * self.n*self.m + otherAgentPos

    def updateQmatrix(self, ):
        pass

    def updateReward(self, reward):
        self.reward = reward


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

    # Sets old position to new
    def setGrid(self, resultingPos, agent):
        x, y = self.getAgentRowAndColumn(agent)
        self.grid[x][y] = 0
        agent.agentPosition = resultingPos
        x, y = self.getAgentRowAndColumn(agent)
        self.grid[x][y] = 1

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
        x, y = self.getAgentRowAndColumn(agent)

        currentState = agent.getState(agent.agentPosition, otherAgentPos)
        resultingPos = agent.agentPosition + self.actionSpace[action]
        resultingState = agent.getState(resultingPos, otherAgentPos)

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
                else:
                    reward = -1
            else:
                reward = 50

            self.setGrid(resultingPos, agent)
            agent.updatePosition(resultingPos)
            agent.updateReward(reward)
            return resultingState, agent.reward, agent.isTerminalState(resultingState), None
        else:
            reward = -1
            agent.updateReward(reward)
            return currentState, agent.reward, agent.isTerminalState(currentState), None

    def reset(self):
        # agent.agentPosition = 0
        self.grid = np.zeros((self.n, self.m))
        # return agent.agentPosition

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


def maxAction(Q, state, actions):
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return actions[action]


n = 4
m = 4
wallsYX = []
agent1 = [(0, 0)]
agent2 = [(3, 0)]
#if __name__ == '__main__':
def main():
    pickupSpot = 2
    dropSpot = 8
    env = Warehouse(n, m)

    ALPHA = 0.1
    GAMMA = 1.0
    EPSILON = 1

    numGames = 500000
    totalRewards = np.zeros((numGames, 2))
    # env.render()
    maxSteps = 500
    steps = 0
    agents = [Agent(0, 15, n, m), Agent(12, 3, n, m)]

    for i in range(numGames):
        if i % 250 == 0:
            print('Starting episode', i)

            done = [False, False]
            epRewards = [0, 0]
            observation = [12, 192]
            observation_ = [0, 0]
            agents[0].reset(0)
            agents[1].reset(12)
            env.reset()
            """
            if i == numGames - 250:
                # Always starts without an item
                for x in env.walls:
                    env.getWalls(x)

                #for x in env.walls:
                    #wallsYX.append(env.getWalls(x))

                env.grid[0][0] = 1
                env.grid[3][0] = 1
                env.render()
            """
            otherAgentPos = 12

            while not (done[0] and done[1]):
                j = 0
                for agent in agents:
                    if done[j]:
                        j += 1
                        otherAgentPos = agent.agentPosition
                        continue

                    rand = np.random.random()
                    action = maxAction(agent.Q, observation[j], env.possibleActions) if rand < (
                                1 - EPSILON) else env.actionSpaceSample()
                    #print(action)

                    observation_[j], reward, done[j], info = env.step(action, agent, otherAgentPos)
                    epRewards[j] += reward
                    #print(j,reward)
                    #print(j,agent.agentPosition)
                    #print(j,done[j])
                    #print(j,otherAgentPos)
                    action_ = maxAction(agent.Q, observation_[j], env.possibleActions)

                    agent.Q[observation[j], action] = agent.Q[observation[j], action] + ALPHA * (
                                reward + GAMMA * agent.Q[observation_[j], action_] - agent.Q[observation[j], action])
                    observation[j] = observation_[j]

                    otherAgentPos = agent.agentPosition

                    # Explore or exploit
                    if EPSILON - 10 / numGames > 0:
                        EPSILON -= 10 / numGames
                    else:
                        EPSILON = 0
                    totalRewards[i][j] = epRewards[j]

                    # Renders the last episode
                    if i == numGames - 250:
                        for x in env.walls:
                            wallsYX.append(env.getWalls(x))
                        if j == 0:
                         agent1.append(env.getAgentRowAndColumn(agents[0]))
                        else:
                            agent2.append(env.getAgentRowAndColumn(agents[1]))
                        #env.render()

                    j += 1

    #plt.plot(totalRewards)
    #plt.show()
    print(EPSILON)
    #print(agent1)
    #print(agent2)
    #print(wallsYX)

