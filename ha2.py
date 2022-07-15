import csv
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tqdm

def plot_CDF(filename):
    title = filename.split('.')[0]
    params = re.findall('\d+', filename)
    params = list(map(int, params))

    n_UEs = params[1]
    epochs = 100

    methods = ['Non-cooperative MRT random', 'Non-cooperative MRT greedy', 'Non-cooperative ZF random', 'Non-cooperative ZF greedy', 'Cooperative MRT random', 'Cooperative MRT greedy', 'Cooperative ZF random', 'Cooperative ZF greedy']
    columns = []
    for i in range(n_UEs * epochs):
        columns.append(i+1)
    values = []

    with open('./data/' + filename, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        cnt = 0
        for line in csv_reader:
            samples = list(map(float, line))
            values.append(samples)
            cnt += 1
    # print(values)
    values = np.array(values)
    # print(np.shape(values))

    fontsize = 10
    msize = 4
    lwidth = 2
    N_markers = 10
    marker_sep = round(n_UEs * epochs/N_markers)
    y_axis = np.arange(1, n_UEs * epochs + 1)/(n_UEs * epochs)

    ## MRT / ZF: r / k
    ## Random / greedy: > / s
    ## Non-cooperative / Cooperative: - / *
    # 'Non-cooperative MRT greedy', 'Non-cooperative MRT random', 'Non-cooperative ZF greedy', 'Non-cooperative ZF random',
    # 'Cooperative MRT greedy', 'Cooperative MRT random', 'Cooperative ZF greedy', 'Cooperative ZF random'
    type = ['rs-', 'r>-', 'ks-', 'k>-', 'rs:', 'r>:', 'ks:', 'k>:']

    for i in range(8):
        values[i].sort()
        plt.plot(values[i], y_axis, type[i], lw=lwidth, ms=msize, markevery=marker_sep, label=methods[i])
    plt.title(title)
    plt.xlim((0.0, 9.0))
    plt.ylim((0.0, 1.0))
    plt.xticks(fontsize=fontsize-2)
    plt.yticks(fontsize=fontsize-2)
    plt.legend(fontsize=fontsize)
    plt.grid()
    plt.xlabel('Spectral efficiency [bps/Hz]', fontsize=fontsize)
    plt.ylabel('CDF', fontsize=fontsize)
    plt.savefig('./fig/' + title + '.png')
    plt.clf()

if __name__ == '__main__':
    import os
    path_dir = './data'
    file_list = os.listdir(path_dir)
    # file_list = file_list[1:]
    print(file_list)
    # plot_CDF("TM50_K10_Q1_N16_tau15.csv")

    for i in tqdm.tqdm(range(len(file_list)), desc='Plotting CDF'):
        plot_CDF(file_list[i])