from QL_1agent_main import *
import matplotlib.pyplot as plt

main()

plt.plot(totalRewards)
plt.xlabel('Episode')
plt.ylabel('Total reward')
plt.title('Q-learning with 1 agents')
plt.show()
