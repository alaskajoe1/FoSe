import matplotlib.pyplot as plt     # standard abbreviation

days = [1, 2, 3, 4, 5]

sleeping = [7, 8, 6, 11, 7]
eating = [2, 3, 4, 3, 2]
working = [7, 8, 7, 2, 2]
playing = [8, 5, 7, 8, 13] # I wish... rip

# makes labels to create a legend (otherwise can't with stackplot)
plt.plot([], [], color='m', label='Sleeping', linewidth=5)
plt.plot([], [], color='c', label='Eating', linewidth=5)
plt.plot([], [], color='r', label='Working', linewidth=5)
plt.plot([], [], color='k', label='Playing', linewidth=5)

plt.stackplot(days, sleeping, eating, working, playing, colors=['m', 'c', 'r', 'k'])

# add x and y labels
plt.xlabel('x')
plt.ylabel('y')

# adds title
plt.title('Interesting Graph\nCheck it out')

# adds legend
plt.legend()

# Show plot
plt.show()




