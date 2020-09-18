import pandas as pd
import json

df = pd.read_csv('../output/pixel_array.csv')

b = '🅱️'
space = len(b)

final_output = ''

for index, row in df.iterrows():
    for entry in row:
        entry = json.loads(entry)
        if int(entry[0])>5 or int(entry[1])>5 or int(entry[2])>5:
            final_output += b
        else:
            final_output += space*' '
    final_output += '\n'

print(final_output)