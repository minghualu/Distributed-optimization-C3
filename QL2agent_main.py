import matplotlib.pyplot as plt
from QL2agent_env import *
from QL2agent_agent import *

def maxAction(Q, state, actions):
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return actions[action]

numGames = 20
totalRewards = np.zeros((numGames, 2))

def main():
    n = 10
    m = 10
    wallsYX = []
    agent1 = [(0, 0)]
    agent2 = [(9, 0)]
    env = Warehouse(n, m)

    ALPHA = 0.1
    GAMMA = 1.0
    EPSILON = 1

    # env.render()
    maxSteps = 500
    steps = 0
    agents = [Agent(0, 99, n, m), Agent(90, 9, n, m)]

    for i in range(numGames):
        if i % 1 == 0:
            print('Starting episode', i)

            done = [False, False]
            epRewards = [0, 0]
            observation = [90, 900]
            observation_ = [0, 0]
            agents[0].reset(0)
            agents[1].reset(90)
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
            otherAgentPos = 90

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
                    if EPSILON - 0.005 / numGames > 0:
                        EPSILON -= 0.005 / numGames
                    else:
                        EPSILON = 0
                    totalRewards[i][j] = epRewards[j]

                    # Renders the last episode
                    if i == numGames - 1:
                        for x in env.walls:
                            wallsYX.append(env.getWalls(x))
                        if j == 0:
                            agent1.append(env.getAgentRowAndColumn(agents[0]))
                        else:
                            agent2.append(env.getAgentRowAndColumn(agents[1]))
                        #env.render()

                    j += 1
