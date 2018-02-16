"""Build a wells configuration string from a CSV file of production figures"""
import os

import pandas as pd

df = pd.read_csv('NENE production.csv', index_col='Date')
df.fillna(0, inplace=True)
oil_df = df.filter(like='Oil', axis=1)
gas_df = df.filter(like='Gas', axis=1)

oil_rates = list(oil_df.iloc[-1])
gas_rates = list(gas_df.iloc[-1])
oil_cums = list(oil_df.sum(axis=0))
gas_cums = list(gas_df.sum(axis=0))

names = []
for label in oil_df.columns:
    name, _ = label.split(' ')
    names.append(name)

data = zip(names, oil_rates, gas_rates, oil_cums, gas_cums)

try:
    os.remove('well_data.txt')
except:
    pass

with open('well_data.txt', 'a') as out_file:
    for d in data:
        name, oil_rate, gas_rate, oil_cum, gas_cum = d
        well_string = """{}:
    type: oil
    oil rate: {:d}
    oil cumulative: {:d}
    gas rate: {:d}
    gas cumulative: {:d}\n""".format(name, int(oil_rate), int(oil_cum), int(gas_rate * 1000000), int(gas_cum * 1000000))
        print(well_string)
        out_file.write(well_string)

# with open('well_data.txt', 'w') as out_file:
#     out_file.write()
