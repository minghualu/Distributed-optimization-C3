import random
import numpy as np
import matplotlib.pyplot as plt
from warehouseclass import *
from agentclass import *
global Q, agentPosition

def main():
    pickupSpot = 2
    dropSpot = 8
    env = Warehouse(10, 10)

    ALPHA = 0.1
    GAMMA = 1.0
    EPSILON = 0.7


    numGames = 5000
    totalRewards = np.zeros((numGames, 2))
    #env.render()
    maxSteps = 500
    steps = 0
    agents = [Agent(0, 99), Agent(90, 9)]

    for i in range(numGames):
        if i % 250 == 0:
            print('starting game', i)

            done = [False, False]
            epRewards = [0, 0]
            observation = [90, 9000]
            observation_ = [0, 0]
            
            otherAgentPos = 90

            while done[0] == False or done[1] == False:
                j = 0
                for agent in agents:
                    rand = np.random.random()
                    action = maxAction(agent.Q, observation[j], env.possibleActions) if rand < (1-EPSILON) else env.actionSpaceSample()
                    print(action)
                
                    observation_[j], reward, done[j], info = env.step(action, agent, otherAgentPos)
                    epRewards[j] += reward
                    print(reward)
                    print(agent.agentPosition)
                    print(done[j])
                    action_ = maxAction(agent.Q, observation_[j], env.possibleActions)
                    
                    agent.Q[observation[j], action] = agent.Q[observation[j], action] + ALPHA*(reward + GAMMA*agent.Q[observation_[j], action_] - agent.Q[observation[j], action])
                    observation[j] = observation_[j]
                    
                    otherAgentPos = agent.agentPosition

                    #Explore or exploit
                    if EPSILON - 2 / numGames > 0:
                        EPSILON -= 2 / numGames
                    else:
                        EPSILON = 0
                    totalRewards[i][j] = epRewards[j]

                    # Renders the last episode
                    if i == numGames - 250:
                        env.render()
                    steps += 1
                    if steps == maxSteps:
                        done = [True, True]
                    
                    j +=1

    plt.plot(totalRewards)
    plt.show()


main()
