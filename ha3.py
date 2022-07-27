import csv
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tqdm

def extract_value(filename):
    params = re.findall('\d+', filename)
    params = list(map(int, params))

    n_UEs = params[1]
    epochs = 100

    columns = []
    for i in range(n_UEs * epochs):
        columns.append(i + 1)
    ret_dict = {}

    list_line = ["_non-coop-MRT", "_non-coop-ZF", "_coop-MRT", "_coop-ZF"]

    with open('./data/' + filename, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        cnt = 0
        for line in csv_reader:
            samples = list(map(float, line))
            if cnt % 2 == 0:
                ret_dict[filename + list_line[cnt//2]] = np.array(samples)
            cnt += 1
    return ret_dict

def select_data(input_dict, select_filter):
    ret_dict = {}
    for key, value in input_dict.items():
        flag = True
        for _filter in select_filter:
            if _filter not in key:
                flag = False
                break
        if flag:
            ret_dict[key] = value
    return ret_dict

def dict_to_list(input_dict):
    # TODO: to be changed
    # key_filter = [["TM50_", "_non-coop"],
    #               ["TM100_", "_non-coop"],
    #               ["TM50_", "_coop"],
    #               ["TM100_", "_coop"]]
    key_filter = [["N1_", "_non-coop"],
                  ["N2_", "_non-coop"],
                  ["N4_", "_non-coop"],
                  ["N8_", "_non-coop"],
                  ["N16_", "_non-coop"],
                  ["N1_", "_coop"],
                  ["N2_", "_coop"],
                  ["N4_", "_coop"],
                  ["N8_", "_coop"],
                  ["N16_", "_coop"]]
    # TODO: END
    ret_values_list = []
    ret_methods_list = []

    for idx in range(len(key_filter)):
        for key, value in input_dict.items():
            flag = True
            for _filter in key_filter[idx]:
                if _filter not in key:
                    flag = False
                    break
            if flag:
                print(key_filter[idx], key)
                ret_values_list.append(value)
                ret_methods_list.append(key_filter[idx][0][:-1] + key_filter[idx][1])
    return np.array(list(ret_values_list)), np.array(list(ret_methods_list))

def plot_CDF(filename, values, methods):
    title = filename
    params = re.findall('K\d+', filename)[0]
    params = params[1:]

    n_UEs = int(params)
    epochs = 100

    columns = []
    for i in range(n_UEs * epochs):
        columns.append(i+1)

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
    # type = ['rs-', 'r>-', 'ks-', 'k>-', 'rs:', 'r>:', 'ks:', 'k>:', 'r', 'k']
    for i in range(len(values)):
        values[i].sort()
        plt.plot(values[i], y_axis, lw=lwidth, ms=msize, markevery=marker_sep, label=methods[i])
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

    data_values = {}
    for i in range(len(file_list)):
        data_values.update(extract_value(file_list[i]))

    for i in range(3):
        num_CPU = str((i+1)**2)
        plot_values_MRT = {}
        # TODO: to be changed
        # select_filter_MRT = ["K20", "Q" + num_CPU, "N16", "tau10", "MRT"]
        # filename_MRT = "K20" + "_" + "Q" + num_CPU + "_" + "N16" + "_" + "tau10" + "_" + "MRT"
        select_filter_MRT = ["TM100", "K20", "Q" + num_CPU, "tau10", "MRT"]
        filename_MRT = "TM100" + "_" + "K20" + "_" + "Q" + num_CPU + "_" + "tau10" + "_" + "MRT"
        # TODO: END
        plot_values_MRT.update(select_data(data_values, select_filter_MRT))
        plot_values_MRT_values_list, plot_values_MRT_methods_list = dict_to_list(plot_values_MRT)
        plot_CDF(filename_MRT, plot_values_MRT_values_list, plot_values_MRT_methods_list)

        plot_values_ZF = {}
        # TODO: to be changed
        # select_filter_ZF = ["K20", "Q" + num_CPU, "N16", "tau10", "ZF"]
        # filename_ZF = "K20" + "_" + "Q" + num_CPU + "_" + "N16" + "_" + "tau10" + "_" + "ZF"
        select_filter_ZF = ["TM100", "K20", "Q" + num_CPU, "tau10", "ZF"]
        filename_ZF = "TM100" + "_" + "K20" + "_" + "Q" + num_CPU + "_" + "tau10" + "_" + "ZF"
        # TODO: END
        plot_values_ZF.update(select_data(data_values, select_filter_ZF))
        plot_values_ZF_values_list, plot_values_ZF_methods_list = dict_to_list(plot_values_ZF)
        plot_CDF(filename_ZF, plot_values_ZF_values_list, plot_values_ZF_methods_list)


    # for i in tqdm.tqdm(range(len(file_list)), desc='Plotting CDF'):
    #     plot_CDF(file_list[i])
