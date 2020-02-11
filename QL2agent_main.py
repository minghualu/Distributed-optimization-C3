from QL2agent_env import *
from QL2agent_agent import *

def maxAction(Q, state, actions):
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return actions[action]

numGames = 2000
totalRewards = np.zeros((numGames, 2))
wallsYX = []
agent1 = [(0, 0)]
agent2 = [(9, 0)]

def main():
    n = 10
    m = 10
    env = Warehouse(n, m)

    ALPHA = 0.1
    GAMMA = 1.0
    EPSILON = 1

    # env.render()
    agents = [Agent(0, 99, n, m), Agent(90, 9, n, m)]

    for i in range(numGames):
        if i % 1 == 0:
            print('Starting episode', i)

            # Explore or exploit
            if EPSILON - 1 / numGames > 0:
                EPSILON -= 1 / numGames
            else:
                EPSILON = 0

            #print(EPSILON)

            done = [False, False]
            epRewards = [0, 0]
            observation_old = [90, 900]
            observation_new = [0, 0]
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
                    action_old = maxAction(agent.Q, observation_old[j], env.possibleActions) if rand < (
                                1 - EPSILON) else env.actionSpaceSample()
                    #print(action)

                    observation_new[j], reward, done[j], info = env.step(action_old, agent, otherAgentPos)
                    epRewards[j] += reward
                    #print(j,reward)
                    #print(j,agent.agentPosition)
                    #print(j,done[j])
                    #print(j,otherAgentPos)
                    action_new = maxAction(agent.Q, observation_new[j], env.possibleActions)

                    agent.Q[observation_old[j], action_old] = agent.Q[observation_old[j], action_old] + ALPHA * (
                                reward + GAMMA * agent.Q[observation_new[j], action_new] - agent.Q[observation_old[j], action_old])
                    observation_old[j] = observation_new[j]

                    otherAgentPos = agent.agentPosition

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

