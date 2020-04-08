import pickle
from tkinter import *

root = Tk()
agent_path = []
agent_path.append([])
agent_path.append([])
step = 0
n = 0
m = 0

def Draw():
    global agent_path, step, n, m
    # n = 10
    # m = 10
    for r in range(n):
        for c in range(m):
            if (r, c) == agent_path[0][step]:
                Label(root, text='A1', height=2, width=4, borderwidth=4, bg='lightblue', relief="groove").grid(row=r, column=c)
            elif (r, c) == agent_path[1][step]:
                Label(root, text='A2', height=2, width=4, borderwidth=4, bg='lightblue', relief="groove").grid(row=r, column=c)
            elif r == n-1 and c == m-1:
                Label(root, text='1', height=3, width=6, borderwidth=4, bg='green', relief="groove").grid(row=r, column=c)
            elif r == 0 and c == m-1:
                Label(root, text='2', height=3, width=6, borderwidth=4, bg='green', relief="groove").grid(row=r, column=c)
            elif r == 0 and c == 0:
                Label(root, height=3, width=6, borderwidth=4, bg='red', relief="groove").grid(row=r, column=c)
            elif r == n-1 and c == 0:
                Label(root, height=3, width=6, borderwidth=4, bg='red', relief="groove").grid(row=r, column=c)
            else:
                Label(root, height=3, width=6, borderwidth=4, bg='grey', relief="groove").grid(row=r,column=c)

def Refresher():
    global step
    Draw()
    step += 1
    if step >= len(agent_path[0]):
        return
    root.after(1000, Refresher)


def testDQL2():
    global agent_path, n, m

    with open('env.pkl', 'rb') as input:
        env = pickle.load(input)
    with open('agents.pkl', 'rb') as input:
        agents = pickle.load(input)

    env.reset()
    n = env.n
    m = env.m
    agent_path[0].append(env.getAgentRowAndColumn(0))
    agent_path[1].append(env.getAgentRowAndColumn(1))

    done = [False, False]
    noSteps = 0
    while not(done[0] and done[1]) and noSteps < 50:
        
        for j in range(2):
        
            # if not done[j]:
            curr_state = env.state.copy()
            action = agents[j].act(curr_state, 0)
            next_state, reward, done[j], info = env.step(action, j)
            agent_path[j].append(env.getAgentRowAndColumn(j))
        
            # print("Agent: {}, action: {}, curr_state: {}, next_state: {}, reward: {}, done: {}, info: {}"
                #       .format(j+1, action, curr_state, next_state, reward, done[j], info))

        # print()
        noSteps += 1

    print("Agent 1: ", agent_path[0])
    print("Agent 2: ", agent_path[1])
    
    Refresher()
    root.mainloop()
    

testDQL2()