from QL_2agent_main import *
import matplotlib.pyplot as plt

main()
plt.plot(totalRewards)
plt.xlabel('Episode')
plt.ylabel('Total reward')
plt.title('Q-learning with 2 agents')
plt.show()
