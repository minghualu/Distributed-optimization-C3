from tkinter import *
from QL2agent_main2 import *
import matplotlib.pyplot as plt


i = 0
j = 0

def Draw(i, j):
    global agent1, agent2, wallsYX
    for r in range(n):
        for c in range(m):
            if (r, c) == agent1[i]:
                Label(root, text='A1', height=2, width=4, borderwidth=4, bg='blue', relief="groove").grid(row=r, column=c)
            elif (r, c) == agent2[j]:
                Label(root, text='A2', height=2, width=4, borderwidth=4, bg='blue', relief="groove").grid(row=r, column=c)
            elif r == n-1 and c == m-1:
                Label(root, text='1', height=3, width=6, borderwidth=4, bg='green', relief="groove").grid(row=r, column=c)
            elif r == 0 and c == m-1:
                Label(root, text='2', height=3, width=6, borderwidth=4, bg='green', relief="groove").grid(row=r, column=c)
            elif r == 0 and c == 0:
                Label(root, height=3, width=6, borderwidth=4, bg='red', relief="groove").grid(row=r, column=c)
            elif r == n-1 and c == 0:
                Label(root, height=3, width=6, borderwidth=4, bg='red', relief="groove").grid(row=r, column=c)
            elif (r, c) in wallsYX:
                Label(root, height=3, width=6, borderwidth=4, bg='black', relief="groove").grid(row=r, column=c)

            #elif c == 1 and r in [0, 1, 2, 3, 4]:
            #    Label(root, height=2, width=4, borderwidth=4, bg='black', relief="groove").grid(row=r,column=c)
            #elif c == 4 and r in [4, 5, 6, 7, 8, 9]:
            #    Label(root, height=2, width=4, borderwidth=4, bg='black', relief="groove").grid(row=r,column=c)
            else:
                Label(root, height=3, width=6, borderwidth=4, bg='grey', relief="groove").grid(row=r,column=c)

def Refresher():
    global i, j
    #print(i)
    Draw(i, j)
    if i + 1 < len(agent1):
        i += 1
    if j + 1 < len(agent2):
        j += 1
    #if i < max(len(agent1), len(agent2)):
    root.after(1000, Refresher)

main()
root=Tk()
Refresher()
root.mainloop()
plt.plot(totalRewards)
plt.show()