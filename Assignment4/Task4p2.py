import time
import csv
import matplotlib.pyplot as plt


with open('Assignment4\hemp.txt') as f:
    reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
    xs, ys = zip(*reader)

print(xs)
print(ys)

plt.plot(xs,ys)
plt.show()