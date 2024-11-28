import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def gini(y_pred, y_true):

    # casting
    y_pred = np.array(y_pred)
    y_true = np.array(y_true)

    # obtain index for sorting according to y_scores
    sorted_idx = np.argsort(y_pred)[::-1]

    # created sorted arrays BY SCORES
    sorted_pred = y_pred[sorted_idx]
    sorted_true = y_true[sorted_idx]

    # calculate lorenz function for different Ks for:
    # our discriminator
    f_k = np.concatenate(([0], (sorted_true == 1).cumsum() / sorted_true.sum()))
    # theoretical perfect model
    f_optimal = np.concatenate(
        ([0], (np.sort(y_true)[::-1]).cumsum() / sorted_true.sum())
    )
    # theoretical random
    f_rand = np.linspace(0, 1, len(f_k))

    # calculate gini
    gini = np.sum(f_k - f_rand)
    gini_optimal = np.sum(f_optimal - f_rand)

    return gini / gini_optimal

def plot_gini(y_pred, y_true):
    # casting
    y_pred = np.array(y_pred)
    y_true = np.array(y_true)

    # obtain index for sorting according to y_scores
    sorted_idx = np.argsort(y_pred)[::-1]

    # created sorted arrays BY SCORES
    sorted_pred = y_pred[sorted_idx]
    sorted_true = y_true[sorted_idx]

    # calculate lorenz function for different Ks for:
    # our discriminator
    f_k = np.concatenate(([0], (sorted_true == 1).cumsum() / sorted_true.sum()))
    # theoretical perfect model
    f_optimal = np.concatenate(([0], (np.sort(y_true)[::-1]).cumsum() / sorted_true.sum()))
    # theoretical random
    f_rand = np.linspace(0, 1, len(f_k))

    plt.figure(figsize=(9,7))
    xs = np.linspace(0, 100, 11)
    plt.scatter(xs, f_k, color='blue')
    plt.plot(xs, f_k, label='My Model', color='blue')
    plt.scatter(xs, f_optimal, color='black')
    plt.plot(xs, f_optimal, color='black', linestyle='dotted', label='Perfect Model')
    plt.scatter(xs, f_rand, color='red')
    plt.plot(xs, f_rand, color='red', linestyle='dotted', label='Random Model')

    plt.xlim(- 5,105 )
    plt.ylim(-0.05,1.05)

    plt.title('Gini Coefficient', fontsize=22)
    plt.xlabel('Cummulative Percent of Population', fontsize=20)
    plt.ylabel('Cummulative Percent of Bads', fontsize=20)
    plt.legend(fontsize=18, loc=2)
    plt.show()



if __name__ == '__main__':
    
    y_pred = [0.29, 0.36, 0.81, 0.31, 0.68, 0.82, 0.90, 0.13, 0.86, 0.97]
    y_true = [0, 1, 0, 0, 1, 1, 1, 0, 0, 1]

    print('Gini Coefficient:', gini(y_pred, y_true))
    plot_gini(y_pred, y_true)