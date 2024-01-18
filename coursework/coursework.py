import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def plot_histogram(slopes):
    slopes = np.array(slopes)
    slopes_filtered = slopes[(slopes > np.quantile(slopes, 0.25)) & (slopes < np.quantile(slopes, 0.75))]
    counts, bin_edges = np.histogram(slopes_filtered, bins=30)
    print(f"max count hist = {max(counts)}")
    plt.hist(slopes_filtered, bins=30, edgecolor='black')
    plt.xlabel("Slope")
    plt.ylabel("Frequency")
    plt.title("Histogram of Slopes, 3-4 column")
    plt.show()

def theil_sen(x, y):
    slopes = []
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            if x[j] - x[i] != 0:
                slope = (y[j] - y[i]) / (x[j] - x[i])
                slopes.append(slope)
    #plot_histogram(slopes)

    median_slope = np.median(slopes)
    min_slope = np.min(slopes)
    max_slope = np.max(slopes)
    mode_slope = stats.mode(slopes)

    return median_slope #, min_slope, max_slope, mode_slope


# Load the data from the file
data = pd.read_csv("TS data.csv", header=None, delimiter=" ")

x = data.iloc[:, 2].values
y = data.iloc[:, 3].values

slopes = theil_sen(x,y)

plt.scatter(x, y, marker='s')
plt.grid()
plt.xlabel("3 столбец")
plt.ylabel("4 столбец")
plt.title("Theil-Sen Estimator")
median_slope = theil_sen(x, y)
print("Slope:", median_slope)

x_line = np.array([min(x), max(x)])
y_line = median_slope * (x_line - min(x))
plt.plot(x_line, y_line, color="red")
plt.plot(x_line, (x_line - min(x))*0.7, color='pink')
plt.plot(x_line, (x_line - min(x))*1.3, color='pink')
plt.show()

#median_slope, min_slope, max_slope, mode_slope = theil_sen(x, y)
# print("Median Slope:", median_slope)
# print("Min Slope:", min_slope)
# print("Max Slope:", max_slope)
# print("Mode Slope:", mode_slope)



def bootstrap_median(x, y, num_bootstraps, confidence_level):
    medians = []
    for _ in range(num_bootstraps):
        indices = np.random.choice(len(x), size=len(x), replace=True)
        x_bootstrap = x[indices]
        y_bootstrap = y[indices]
        median_bootstrap = np.median(y_bootstrap)
        medians.append(median_bootstrap)

    medians = np.array(medians)
    lower_quantile = (1 - confidence_level) / 2
    upper_quantile = 1 - lower_quantile
    lower_ci = np.quantile(medians, lower_quantile)
    upper_ci = np.quantile(medians, upper_quantile)
    variability_estimate = (upper_ci - lower_ci) / 2

    return variability_estimate

# Заданные параметры
confidence_level = 0.95
num_bootstraps = 1000

# Вызов функции и вывод результата
variability_estimate = bootstrap_median(x, y, num_bootstraps, confidence_level)
print(f"Оценка вариабельности медианы на доверительном уровне {confidence_level}: {variability_estimate}")


