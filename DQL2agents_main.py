from DQL_new_env import *
from DQL_agentclass import *
# from testDQL import *
import matplotlib.pyplot as plt
import pickle

def main():
    n = 5
    m = 5
    NumGames = 100
    NumTimes = 100
    epsilon = 1
    epsilon_min = 0.01
    env = Warehouse(n, m, 0, (m-1)*n, n*m-1, m-1)   # Start in upper and lower left and ending in the other end of the diagonals
    # env = Warehouse(n, m, 0, 12, 15, 3)
    # env = Warehouse(n, m, 0, 20, 24, 4)
    #state_size = 100 
    state_size = n*m 
    action_size = 4
    agents = [DQNAgent(state_size, action_size), DQNAgent(state_size, action_size)]
    #done = False
    batch_size = 32
    totalReward = np.zeros(NumGames)

    for i in range(NumGames):
        replays = [0, 0]
        epRewards = 0
        env.reset()
        # print()
        # print("Game number: {}, Initial state: {}".format(i+1, env.state), end = '')
        done = [False, False]
        for time in range(NumTimes):
            #print(time)
            for j in range(2):
                if done[j]:
                    continue
                #env.render()
                curr_state = env.state.copy()
                action = agents[j].act(curr_state, epsilon)
                next_state, reward, done[j], info = env.step(action, j)
                # print("Agent: {}, action: {}, curr_state: {}, next_state: {}, reward: {}, done: {}, info: {}"
                #       .format(j+1, action, curr_state, next_state, reward, done[j], info))
                #reward = reward if not done else -10
                #next_state = np.reshape(next_state, [1, state_size])
                agents[j].memorize(curr_state, action, reward, next_state, done[j])
                epRewards += reward

                # If the agents have collided
                if info == True:
                    break
                
                if len(agents[j].memory) > batch_size:
                    # print('Replay agent #{}'.format(j+1))
                    replays[j] += 1
                    agents[j].replay(batch_size)
            
            if (done[0] and done[1]) or info == True:
                break

        if epsilon > epsilon_min:
            epsilon -= 1/NumGames
            if epsilon < epsilon_min:
                epsilon = epsilon_min

        totalReward[i] = epRewards
        print("Game: {}/{}, \t epRewards: {:3}, \t done: {}, \t collided: {}, \t time: {:3}, \t replays: {},   \t epsilon: {:.2}"
              .format(i+1, NumGames, epRewards, done, info, time, replays, epsilon))

    with open('env.pkl', 'wb') as output:  # Overwrites any existing file.
        pickle.dump(env, output, pickle.HIGHEST_PROTOCOL)
    with open('agents.pkl', 'wb') as output:  # Overwrites any existing file.
        pickle.dump(agents, output, pickle.HIGHEST_PROTOCOL)

    plt.plot(totalReward)
    plt.show()
    
    # testDQL2(agents, env)


main()