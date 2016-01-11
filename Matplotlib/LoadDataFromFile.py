import matplotlib.pyplot as plt     # standard abbreviation
import numpy as np
import csv

x = []
y = []

'''
# reads in text file (method 1)
with open('example.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

# plots loaded in data
plt.plot(x, y, label='Loaded from file')
'''

#method 2
x, y = np.loadtxt('example.txt', delimiter=',', unpack=True)
# plots loaded in data
plt.plot(x, y, label='Loaded from file')


# adds title
plt.title('Interesting Graph\nCheck it out')

# add x and y labels
plt.xlabel('x')
plt.ylabel('y')

# adds a legend
plt.legend()

# Show plot
plt.show()




