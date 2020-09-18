import pandas as pd
import json

df = pd.read_csv('../output/pixel_array.csv')

final_output = ''

for index, row in df.iterrows():
    for entry in row:
        entry = json.loads(entry)
        if int(entry[0])>5 or int(entry[1])>5 or int(entry[2])>5:
            final_output += '🅱️'
        else:
            final_output += '\t'
    final_output += '\n'

print(final_output)