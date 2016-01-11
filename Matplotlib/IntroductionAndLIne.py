import matplotlib.pyplot as plt     # standard abbreviation

x = [1, 2, 3]
y = [5, 7, 4]

x2 = [1, 2, 3]
y2 = [10, 14, 12]

# create plot
# labels are what show up in the legend
plt.plot(x, y, label='First Line')
plt.plot(x2, y2, label='Second Line')

# add x and y labels
plt.xlabel('Plot Number')
plt.ylabel('Important var')

# adds title
plt.title('Interesting Graph\nCheck it out')

# adds legend
plt.legend()

# Show plot
plt.show()
