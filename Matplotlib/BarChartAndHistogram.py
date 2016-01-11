import matplotlib.pyplot as plt     # standard abbreviation


x = [2, 4, 6, 8, 10]
y = [6, 7, 8, 2, 4]

x2 = [1, 3, 5, 7, 9]
y2 = [7, 8, 2, 4, 2]

# plots bar graph with label (for legend) and colors (can use name, letter or hex colors)
plt.bar(x, y, label='Bars1', color='r')
plt.bar(x2, y2, label='Bars2', color='c')

population_ages = [22, 55, 62, 25, 21, 2, 34, 42, 42, 4, 4, 99, 102, 110, 120, 121, 122, 130, 111, 115, 112, 80, 75, 65, 54, 44, 43, 42, 48]

bins = [0, 20, 40, 60, 80, 100, 120]
#plt.hist(population_ages, bins, histtype='bar', rwidth=0.8)
#plt.show()


# add x and y labels
plt.xlabel('x')
plt.ylabel('y')

# adds title
plt.title('Interesting Graph\nCheck it out')

# adds legend
plt.legend()

# Show plot
#plt.show()




