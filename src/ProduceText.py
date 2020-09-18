# -*- coding: utf-8 -*-

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


with open('../output/bartist.txt','w+', encoding='utf-8') as file:
    file.write(final_output)
    file.close()