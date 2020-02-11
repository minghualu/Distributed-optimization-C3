from QL1agent.QL1agent_env import *

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
            observation_old = env.reset()
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
                action_old = maxAction(Q, observation_old, env.possibleActions) if rand < (
                            1 - EPSILON) else env.actionSpaceSample()
                observation_new, reward, done, info = env.step(action)
                epRewards += reward

                action_new = maxAction(Q, observation_new, env.possibleActions)
                Q[observation_old, action_old] = Q[observation_old, action_old] + ALPHA * (
                            reward + GAMMA * Q[observation_new, action_new] - Q[observation_old, action_old])
                observation_old = observation_new

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

            # Explore or exploit
            if EPSILON - 1 / numGames > 0:
                EPSILON -= 1 / numGames
            else:
                EPSILON = 0
