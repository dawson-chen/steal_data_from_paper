import re
import pandas as pd
import numpy as np


dots = []
with open('./llama3.1_paper_content.txt', 'r', encoding='utf-8', errors='replace') as f:
    fig_content_start = False
    cur_coords = [0, 0]
    group_start = False

    i = 0
    for line in f:
        i += 1
        if re.findall(r'/BBox .*isoflops.pdf', line) and not fig_content_start:
            fig_content_start = True
        
        if not fig_content_start:
            continue
        if re.findall('^endobj$', line):
            break
        
        if re.findall(r'0 J [0-9\.]+ [0-9\.]+ [0-9\.]+ rg 1 w ', line):
            group_start = True
            # print(1)
            cur_coords = [0, 0]

        elif group_start and re.findall(r'cm /M\d+ Do$', line):
            splits = line.split()
            cur_coords[0] += float(splits[-5])
            cur_coords[1] += float(splits[-4])
            dots.append((*cur_coords, splits[-2], ))
        
        elif re.findall(r'^Q$', line):
            group_start = False

# collect from pdf
x_ticks = {
    10 : 172.157532, 
    11 : 293.923456,
    12 : 415.68938
}
y_ticks = {
    0.7 : 68.708327,
    0.75 : 117.758176,
    0.80: 166.808025,
    0.85: 215.857875,
    0.90: 264.907724,
    0.95: 313.957573
}


coefficients = np.polyfit(list(x_ticks.values()), list(x_ticks.keys()), 1)
x_coord_map = np.poly1d(coefficients)
print('x coordinate fit error', np.mean(x_coord_map(list(x_ticks.values())) - np.array(list(x_ticks.keys()))) )

# Perform linear regression
coefficients = np.polyfit(list(y_ticks.values()), list(y_ticks.keys()), 1)
y_coord_map = np.poly1d(coefficients)

print('y coordinate fit error', np.mean(y_coord_map(list(y_ticks.values())) - np.array(list(y_ticks.keys()))) )


mark_map = {'/M9': 6e18, '/M8': 1e19, '/M7': 3e19, '/M6': 6e19, '/M5': 1e20, '/M4': 3e20, '/M3': 6e20, '/M2': 1e21, '/M1': 3e21, '/M0': 1e22, '/M10': 0}

rows = []
for x_coord, y_coord, mark in dots:
    x = x_coord_map(x_coord)
    y = y_coord_map(y_coord)
    
    flops = mark_map[mark]
    rows.append((10**x, y, flops))


isoflops_data = pd.DataFrame(rows, columns=['training tokens', 'val loss', 'flops'])