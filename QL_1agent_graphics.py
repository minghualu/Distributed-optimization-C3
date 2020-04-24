from tkinter import *
from QL_1agent_main import *

i = 0

def Draw(i):
    global agentYX, wallsYX
    for r in range(10):
        for c in range(10):
            if (r, c) == agentYX[i]:
                Label(root, text='Agent', height=2, width=4, borderwidth=4, bg='blue', relief="groove").grid(row=r, column=c)
            elif r == 9 and c == 9:
                Label(root, height=2, width=4, borderwidth=4, bg='green', relief="groove").grid(row=r, column=c)
            elif r == 0 and c == 0:
                Label(root, height=2, width=4, borderwidth=4, bg='red', relief="groove").grid(row=r, column=c)
            elif (r, c) in wallsYX:
                Label(root, height=2, width=4, borderwidth=4, bg='black', relief="groove").grid(row=r, column=c)

            #elif c == 1 and r in [0, 1, 2, 3, 4]:
            #    Label(root, height=2, width=4, borderwidth=4, bg='black', relief="groove").grid(row=r,column=c)
            #elif c == 4 and r in [4, 5, 6, 7, 8, 9]:
            #    Label(root, height=2, width=4, borderwidth=4, bg='black', relief="groove").grid(row=r,column=c)
            else:
                Label(root, height=2, width=4, borderwidth=4, bg='grey', relief="groove").grid(row=r,column=c)


def Refresher():
    global i
    print(i)
    Draw(i)
    i += 1
    if i < len(agentYX):
        root.after(10, Refresher)

main()
root=Tk()
Refresher()
root.mainloop()
