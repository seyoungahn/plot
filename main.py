import csv
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

filename = 'TM50_K10_Q1_N16_tau15.csv'
params = re.findall('\d+', filename)
params = list(map(int, params))

n_APs = params[0]
n_UEs = params[1]
n_CPUs = params[2]
n_Antennas = params[3]
pilot_len = params[4]

idx = ['Non-cooperative MRT greedy', 'Non-cooperative MRT random', 'Non-cooperative ZF greedy', 'Cooperative ZF random', 'Cooperative MRT greedy', 'Cooperative MRT random', 'Cooperative ZF greedy', 'Cooperative ZF random']
columns = []
for i in range(n_UEs):
    columns.append("UE #{}".format(i+1))
data = []
values = []

# with open('./data/' + filename, 'r', encoding='utf-8') as f:
#     csv_reader = csv.reader(f)
#     cnt = 0
#     for line in csv_reader:
#         line = list(map(float, line))
#         data += line
#         s = pd.Series(line, name='value')
#         d = pd.DataFrame(s)
#         sns.distplot(line, kde_kws={'cumulative': True})
#         df.append(s)
#         cnt += 1

with open('./data/' + filename, 'r', encoding='utf-8') as f:
    csv_reader = csv.reader(f)
    cnt = 0
    for line in csv_reader:
        samples = list(map(float, line))
        values.append(samples)
        data += line
        cnt += 1

df = pd.DataFrame(values, columns=columns)
print(df)

data2 = list(map(float, data))
min_value = min(data)
max_value = max(data)

print("MIN VALUE: {}".format(min_value))
print("MAX VALUE: {}".format(max_value))
plt.xlim(min_value, max_value)
plt.ylim(0.0, 1.0)

sns.displot(df, x='Spectral efficiency [bps/Hz]', hue="Methods", kind="ecdf")

# stats = []
# for i in range(1):
#     print(df[i])
#     # Frequency
#     stats_df = df[i].groupby('value')['value'].agg('count').pipe(pd.DataFrame).rename(columns={'value': 'frequency'})
#     # PDF
#     stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
#     # CDF
#     stats_df['cdf'] = stats_df['pdf'].cumsum()
#     stats_df = stats_df.reset_index()
#     print(stats_df)

plt.show()