from DQL_4agents_env import *
from DQL_agentclass import *
import matplotlib.pyplot as plt

def main():
    n = 10
    m = 10
    NumGames = 10000
    epsilon = 1
    epsilon_min = 0.01
    #(rad, kolumn, start1, start2, start3, start4, mål1, mål2, mål3, mål4)
    env = Warehouse(n, m, 0, n*(m-1), n-1, n*m-1, n*m-1, n-1, n*(m-1), 0)
    #state_size = n*m 
    state_size = 4
    action_size = 4
    agents = [DQNAgent(state_size, action_size), DQNAgent(state_size, action_size), DQNAgent(state_size, action_size), DQNAgent(state_size, action_size)]
    #done = False
    batch_size = 32
    totalReward = np.zeros(NumGames)

    for i in range(NumGames):
        replays = [0, 0, 0, 0]
        epRewards = 0
        env.reset()
        # print()
        # print("Game number: {}, Initial state: {}".format(i+1, env.state), end = '')
        done = [False, False, False, False]
        info = [False, False, False, False]
        for time in range(100):
            #print(time)
            for j in range(4):
                if done[j] or info[j]:
                    continue
                #env.render()
                #curr_state = env.state.copy()
                curr_state = [env.agentsPos[0], env.agentsPos[1], env.agentsPos[2], env.agentsPos[3]]
                curr_state = np.reshape(curr_state, [1, state_size])
                action = agents[j].act(curr_state, epsilon)
                next_state, reward, done[j], info[j], otherAgentNr = env.step(action, j)
                next_state = [env.agentsPos[0], env.agentsPos[1], env.agentsPos[2], env.agentsPos[3]]
                next_state = np.reshape(next_state, [1, state_size])
                
                #print("Agent: {}, action: {}, curr_state: {}, next_state: {}, reward: {}, done: {}, info: {}"
                #       .format(j+1, action, curr_state, next_state, reward, done[j], info))
                #reward = reward if not done else -10
                #next_state = np.reshape(next_state, [1, state_size])
                
                agents[j].memorize(curr_state, action, reward, next_state, done[j])
                epRewards += reward
                
                if otherAgentNr != None:
                    info[int(otherAgentNr)-1] = True

                # If the agents have collided
                if info[j]:
                    continue
                
                if len(agents[j].memory) > batch_size:
                    # print('Replay agent #{}'.format(j+1))
                    replays[j] += 1
                    agents[j].replay(batch_size)
            
            if (done[0] and done[1] and done[2] and done[3]) or (info[0] and info[1] and info[2] and info[3]):
                break

        if epsilon > epsilon_min:
            epsilon -= 1/NumGames
            if epsilon < epsilon_min:
                epsilon = epsilon_min

        totalReward[i] = epRewards
        print("Game: {}/{}, \t epRewards: {:3}, \t done: {}, \t collided: {}, \t time: {:3}, \t replays: {},   \t epsilon: {:.2}"
              .format(i+1, NumGames, epRewards, done, info, time, replays, epsilon))

    plt.plot(totalReward)
    plt.show()
    
    #testDQL2(agents, env)


main()
