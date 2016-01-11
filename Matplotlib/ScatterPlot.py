import matplotlib.pyplot as plt     # standard abbreviation

x = [1, 2, 3, 4, 5, 6, 7, 8]
y = [5, 2, 4, 2, 1, 4, 5, 2]

# x's, y's, label, color, marker style, size
plt.scatter(x, y, label='skitscat', color='k', marker='*', s=100)


# add x and y labels
plt.xlabel('x')
plt.ylabel('y')

# adds title
plt.title('Interesting Graph\nCheck it out')

# adds legend
plt.legend()

# Show plot
plt.show()




