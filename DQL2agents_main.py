from DQL_new_env import *
from DQL_agentclass import *

def main():
    n = 10
    m = 10
    NumGames = 100
    env = Warehouse(n, m, 0, 90, 99, 9)
    state_size = 100 
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32
    totalReward = np.zeros(NumGames)

    for i in range(NumGames):
        epRewards = 0
        env.reset()
        state = env.state
        state = np.reshape(state, [1, state_size])
        for time in range(500):
            for j in range(2):
                #env.render()
                action = agent.act(state)
                next_state, reward, done, info = env.step(action, j)
                #reward = reward if not done else -10
                next_state = np.reshape(next_state, [1, state_size])
                agent.memorize(state, action, reward, next_state, done)
                state = next_state
                epRewards += reward
                totalReward[i] = epRewards

                if info == 1:
                    break
                if done:
                    print(i, epRewards)
                    break
                if len(agent.memory) > batch_size:
                    agent.replay(batch_size)

main()