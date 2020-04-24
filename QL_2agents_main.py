from QL_2agents_env import *
from QL_2agents_agent import *

def maxAction(Q, state, actions):
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return actions[action]

#Defining variables
numGames = 200000
totalRewards = np.zeros((numGames, 1))
wallsYX = []
n = 10
m = 10
agent1 = [(0, 0)]
agent2 = [(n - 1, 0)]

def main():
    env = Warehouse(n, m)

    ALPHA = 0.1
    GAMMA = 1.0
    EPSILON = 1

    #Creating agents
    agents = [Agent(0, (n * m) - 1, n, m), Agent((n - 1) * m, m - 1, n, m)]

    #Running all the eppisodes
    for i in range(numGames):
        if i % 1000 == 0:
            print('Starting episode', i)

        #Decreasing epsilon
        if EPSILON - 1 / numGames > 0:
            EPSILON -= 1 / numGames
        else:
            EPSILON = 0

        #Resetting variables
        done = [False, False]
        epRewards = 0
        observation_old = [(n - 1) * m, (n - 1) * m * n * m]
        observation_new = [0, 0]
        agents[0].reset(0)
        agents[1].reset((n - 1) * m)
        env.reset()

        #List of the other agents position
        pos_list = [(n - 1) * m, 0]
        pos_list_temp = [0, 0]
        temp = [0,0,0,0,0,0,0,0]
        info = None

        #Running untill both agents are done
        while not (done[0] and done[1]):
            j = 0
            
            #Breaking episode if agents have collided
            if info == 1:
                break
            
            #One agent taking a step each time
            for agent in agents:
                
                otherAgentPos = pos_list[j]
                
                #If one agent is done
                if done[j]:
                    j += 1
                    #otherAgentPos = agent.agentPosition
                    continue

                rand = np.random.random()
                action_old = maxAction(agent.Q, observation_old[j], env.possibleActions) if rand < (
                            1 - EPSILON) else env.actionSpaceSample()

                observation_new[j], reward, done[j], info = env.step(action_old, agent, otherAgentPos)
                epRewards += reward
                #print(info)

                action_new = maxAction(agent.Q, observation_new[j], env.possibleActions)

                agent.Q[observation_old[j], action_old] = agent.Q[observation_old[j], action_old] + ALPHA * (
                            reward + GAMMA * agent.Q[observation_new[j], action_new] - agent.Q[observation_old[j], action_old])
                ###
                if j == 0:
                    temp[0] = observation_old[0]
                    temp[2] = action_old
                    temp[4] = observation_new[0]
                    temp[6] = action_new
                if j == 1:
                    temp[1] = observation_old[1]
                    temp[3] = action_old
                    temp[5] = observation_new[1]
                    temp[7] = action_new
                ###
                observation_old[j] = observation_new[j]

                totalRewards[i] = epRewards
                
                #Breaking episode if agents have collided
                if info == 1:
                    break

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
            # Update the agents posisions after both agents have steped
            pos_list = [agents[1].agentPosition, agents[0].agentPosition]
            if pos_list_temp[0] == pos_list[1] and pos_list_temp[1] == pos_list[0]:
                reward = -100
                agents[0].Q[temp[0], temp[2]] = agents[0].Q[temp[0], temp[2]] + ALPHA * (
                            reward + GAMMA * agents[0].Q[temp[4], temp[6]] - agents[0].Q[temp[0], temp[2]])
                agents[1].Q[temp[1], temp[3]] = agents[1].Q[temp[1], temp[3]] + ALPHA * (
                            reward + GAMMA * agents[1].Q[temp[5], temp[7]] - agents[1].Q[temp[1], temp[3]])
                info = 1



            pos_list_temp = pos_list
        #print('i', i)
