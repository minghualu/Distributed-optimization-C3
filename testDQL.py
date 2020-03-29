def testDQL2(agents, env):
    
    done = [False, False]
    env.reset()
    noSteps = 0
    
    k = 0

    while not(done[0] and done[1]) and noSteps < 50:
        
        for j in range(2):
        
            if not done[j]:
                curr_state = env.state.copy()
                action = agents[j].act(curr_state, 0)
                next_state, reward, done[j], info = env.step(action, j)
                # agent_path[j].append(env.getAgentRowAndColumn(j))
                k += 1
            
                print("Agent: {}, action: {}, curr_state: {}, next_state: {}, reward: {}, done: {}, info: {}"
                      .format(j+1, action, curr_state, next_state, reward, done[j], info))

        print()
        noSteps += 1

