import matplotlib.pyplot as plt
import numpy as np
"""
# example 1
xpoints = np.array([1, 2, 6, 8])
ypoints = np.array([3, 8, 1, 10])

plt.plot(xpoints, ypoints)
plt.show()

# example 2
plt.plot(xpoints, ypoints, '*')
# * instead of default line
plt.show()

# example 3
# uses 0, 1, 2, 3, ... as x defaults
plt.plot(ypoints)
plt.show()
"""
# example 4
plt.plot([0,0.5],[3,3], marker = 11, markevery=[1], c="purple", markersize=10)
plt.plot([0.5,1],[3,3], marker = 11, markevery=[], c="purple")
plt.show()

# example 4
plt.plot([3,3],[0,0.5], marker = 11, markevery=[0], c="purple", markersize=10)
plt.plot([2,2],[0,1], marker = 11, markevery=[0], c="purple", markersize=10)
plt.axis('equal')
plt.show()
"""
# example 5
plt.plot(ypoints, '*-.g')
plt.show()

# example 6
plt.plot(ypoints, marker = 'o', ms = 20, mec = 'r')
plt.show()

# example 7
plt.plot(ypoints, linestyle = ':')
plt.show()

plt.plot(ypoints, ls = ':')
plt.show()

# example 8
plt.plot(ypoints, linewidth = '20.5', c = 'hotpink')
plt.show()

# example 9
x1 = np.array([0, 1, 2, 3])
y1 = np.array([3, 8, 1, 10])
x2 = np.array([0, 1, 2, 3])
y2 = np.array([6, 2, 7, 11])
# or default values for x-axis
plt.plot(x1, y1, x2, y2)
plt.show()

# example 10
x = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120, 125])
y = np.array([240, 250, 260, 270, 280, 290, 300, 310, 320, 330])

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.title("Sports Watch Data", fontdict = font1,  loc = 'left')
plt.xlabel("Average Pulse", fontdict = font2)
plt.ylabel("Calorie Burnage", fontdict = font2,  loc = 'bottom')

plt.plot(x, y)
plt.show()

# example 11
plt.plot(ypoints, marker = 'o')
plt.grid(color = 'green', axis = 'y')
plt.show()

plt.plot(ypoints, marker = 'o')
plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
plt.show()

# example 11
plt.plot(ypoints, marker = 'o')
plt.show()

# example 12
line1, = plt.plot([1, 2, 3], label='label1')
line2, = plt.plot([1, 8, 4], label='label2')
plt.legend(handles=[line1, line2], loc='lower left')
plt.show()

# example 13
plt.plot([1, 2, 3], label='Inline label') # without lable --> legend empty
plt.legend()
plt.show()

# example 14
#plot 1:
x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])

plt.subplot(1, 2, 1)
plt.plot(x,y)
plt.title("SALES")

#plot 2:
x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])

plt.subplot(1, 2, 2)
plt.plot(x,y)
plt.title("INCOME")

plt.suptitle("MY SHOP")
plt.show()

# example 15
#day one, the age and speed of 13 cars:
x = np.array([5,7,8,7,2,17,2,9,4,11,12,9,6])
y = np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])
plt.scatter(x, y)

#day two, the age and speed of 15 cars:
x = np.array([2,2,8,1,15,8,12,9,7,3,11,4,7,14,12])
y = np.array([100,105,84,105,90,99,90,95,94,100,79,112,91,80,85])
plt.scatter(x, y)

plt.show()

# example 16
data1 = np.random.randn(1000)
data2 = np.random.randn(1000)

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0][0].hist(data1, bins=30, color='blue', edgecolor='black')
axs[0][0].set_title('Histogram 1')
axs[0][0].set_xlabel('Value')
axs[0][0].set_ylabel('Frequency')

axs[0][1].hist(data1, bins=30, color='blue', edgecolor='black')
axs[0][1].set_title('Histogram 2')
axs[0][1].set_xlabel('Value')
axs[0][1].set_ylabel('Frequency')

axs[1][0].hist(data2, bins=30, color='green', edgecolor='black')
axs[1][0].set_title('Histogram 3')
axs[1][0].set_xlabel('Value')
axs[1][0].set_ylabel('Frequency')

axs[1][1].hist(data2, bins=30, color='green', edgecolor='black')
axs[1][1].set_title('Histogram 4')
axs[1][1].set_xlabel('Value')
axs[1][1].set_ylabel('Frequency')

plt.tight_layout(pad=5, w_pad=10, h_pad=0)
plt.show()
"""