from DQL_4agents_env import *
from DQL_agentclass import *
from testDQL import *
import matplotlib.pyplot as plt

def main():
    n = 4
    m = 4
    NumGames = 100
    epsilon = 1
    epsilon_min = 0.01
    #(rad, kolumn, start1, start2, start3, start4, mål1, mål2, mål3, mål4)
    env = Warehouse(n, m, 0, n*(m-1), n-1, n*m-1, n*m-1, n-1, n*(m-1), 0)
    state_size = n*m 
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
        for time in range(100):
            #print(time)
            for j in range(4):
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
            
            if (done[0] and done[1] and done[2] and done[4]) or info == True:
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
