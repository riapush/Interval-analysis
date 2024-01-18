import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def plot_histogram(slopes):
    plt.hist(slopes, bins=10, edgecolor='black')
    plt.xlabel("Slope")
    plt.ylabel("Frequency")
    plt.title("Histogram of Slopes, 1-2 column")
    plt.show()

# Load the data from the file
data = pd.read_csv("TS data.csv", header=None, delimiter=" ")

x = data.iloc[:, 0].values
y = data.iloc[:, 1].values

# Calculate slopes
slopes = []
for i in range(len(x)):
    for j in range(i + 1, len(x)):
        if x[j] - x[i] != 0:
            slope = (y[j] - y[i]) / (x[j] - x[i])
            slopes.append(slope)

# Plot histogram
plot_histogram(slopes)