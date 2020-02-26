from DQL_new_env import *
from DQL_agentclass import *

def main():
    n = 10
    m = 10
    NumGames = 1000
    env = Warehouse(n, m, 0, 90, 99, 9)
    state_size = 100 
    action_size = 4
    agents = [DQNAgent(state_size, action_size), DQNAgent(state_size, action_size)]
    #done = False
    batch_size = 32
    totalReward = np.zeros(NumGames)

    for i in range(NumGames):
        epRewards = 0
        env.reset()
        state = env.state
        state = np.reshape(state, [1, state_size])
        done = [False, False]
        for time in range(1000):
            #print(time)
            for j in range(2):
                if done[j]:
                    continue
                #env.render()
                action = agents[j].act(state)
                next_state, reward, done[j], info = env.step(action, j)
                #reward = reward if not done else -10
                next_state = np.reshape(next_state, [1, state_size])
                agents[j].memorize(state, action, reward, next_state, done[j])
                state = next_state
                epRewards += reward
                totalReward[i] = epRewards

                #If the agents have collided
                if info == 1:
                    break
                
                if len(agents[j].memory) > batch_size:
                    #print('memory')
                    agents[j].replay(batch_size)
            
            #If the agents have collided           
            if info == 1:
                print(i, epRewards)
                break
            if (done[0] and done[1]):
                print(i, epRewards)
                break

main()