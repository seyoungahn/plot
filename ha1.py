import csv
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import interpolate

filename = 'TM50_K40_Q1_N16_tau15.csv'
params = re.findall('\d+', filename)
params = list(map(int, params))

n_APs = params[0]
n_UEs = params[1]
n_CPUs = params[2]
n_Antennas = params[3]
pilot_len = params[4]

methods = ['Non-cooperative MRT greedy', 'Non-cooperative MRT random', 'Non-cooperative ZF greedy', 'Cooperative ZF random', 'Cooperative MRT greedy', 'Cooperative MRT random', 'Cooperative ZF greedy', 'Cooperative ZF random']
columns = ["Methods", "Spectral efficiency [bps/Hz]"]
columns2 = []
for i in range(n_UEs):
    columns2.append("UE #{}".format(i+1))
values = []
values2 = []

with open('./data/' + filename, 'r', encoding='utf-8') as f:
    csv_reader = csv.reader(f)
    cnt = 0
    for line in csv_reader:
        samples = list(map(float, line))
        values2.append(samples)
        for sample in samples:
            values.append([methods[cnt], sample])
        cnt += 1
print(values2)
df = pd.DataFrame(values, columns=columns)
df2 = pd.DataFrame(values2, columns=columns2)
print(df2)
sns.ecdfplot(df, x='Spectral efficiency [bps/Hz]', hue="Methods")
# for i in range(8):
#     sns.kdeplot(data=values2[i], label='Spectral efficiency [bps/Hz]', cumulative=True)

plt.show()