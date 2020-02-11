import matplotlib.pyplot as plt
from QL1agent_env import *

def maxAction(Q, state, actions):
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return actions[action]


agentYX = [(0, 0)]
wallsYX = []
numGames = 1000
totalRewards = np.zeros(numGames)

def main():
    global agentYX

    pickupSpot = 2
    dropSpot = 8
    env = Warehouse(10, 10)

    ALPHA = 0.1
    GAMMA = 1.0
    EPSILON = 0.1

    Q = {}
    for state in env.stateSpacePlus:
        for action in env.possibleActions:
            Q[state, action] = 0

    # env.render()
    maxSteps = 200
    steps = 0

    for i in range(numGames):
        if i % 1 == 0:
            print('starting game', i)

            done = False
            epRewards = 0
            observation = env.reset()
            if i == numGames - 1:
                # Always starts without an item
                """
                for x in env.walls:
                    wallsYX.append(env.getWalls(x))

                env.grid[0][0] = 1
                env.render()
                """

            while not done:
                rand = np.random.random()
                action = maxAction(Q, observation, env.possibleActions) if rand < (
                            1 - EPSILON) else env.actionSpaceSample()
                observation_, reward, done, info = env.step(action)
                epRewards += reward

                action_ = maxAction(Q, observation_, env.possibleActions)
                Q[observation, action] = Q[observation, action] + ALPHA * (
                            reward + GAMMA * Q[observation_, action_] - Q[observation, action])
                observation = observation_

                # Explore or exploit
                if EPSILON - 2 / numGames > 0:
                    EPSILON -= 2 / numGames
                else:
                    EPSILON = 0
                totalRewards[i] = epRewards

                # Renders the last episode
                if i == numGames - 1:
                    """
                    env.render()
                    """
                    for x in env.walls:
                        wallsYX.append(env.getWalls(x))
                    agentYX.append(env.getAgentRowAndColumn())
                steps += 1
                if steps == maxSteps:
                    done = True
