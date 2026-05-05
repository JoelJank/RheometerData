import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from Functions.functions import read_data, split_dataframe, fitting, linfunc, extract_water_content, extract_pressure, mu_to_phi, phi_to_mu
import os
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

plt.style.use('computermodernstyle.mplstyle')

mgs_original = ["../Data/MGS/9kPa/w0per_dried/mohr_coulomb.csv",
                "../Data/MGS/9kPa/w10per_mixed/mohr_coulomb.csv",
                "../Data/MGS/9kPa/w20per_mixed/mohr_coulomb.csv",]
jsc_original = ["../Data/JSC/9kPa/w0per_dried/mohr_coulomb.csv",
                "../Data/JSC/9kPa/w10per_mixed/mohr_coulomb.csv",
                "../Data/JSC/9kPa/w20per_mixed/mohr_coulomb.csv"]

datafiles_mgs = {}
datafiles_jsc = {}

for filepath in mgs_original:
    parts = os.path.normpath(filepath).split(os.sep)
    name = f"{parts[-4]}_{parts[-2]}" 
    data = read_data(filepath)
    data_split = split_dataframe(data, name)
    datafiles_mgs.update(data_split)

for filepath in jsc_original:
    parts = os.path.normpath(filepath).split(os.sep)
    name = f"{parts[-4]}_{parts[-2]}" 
    data = read_data(filepath)
    data_split = split_dataframe(data, name)
    datafiles_jsc.update(data_split)


mgs_fit0per = fitting([datafiles_mgs["MGS_w0per_dried_3kPa"]["Normal_Stress"],
                       datafiles_mgs["MGS_w0per_dried_6kPa"]["Normal_Stress"],
                       datafiles_mgs["MGS_w0per_dried_9kPa"]["Normal_Stress"]],
                      [datafiles_mgs["MGS_w0per_dried_3kPa"]["Shear_Stress"],
                       datafiles_mgs["MGS_w0per_dried_6kPa"]["Shear_Stress"],
                       datafiles_mgs["MGS_w0per_dried_9kPa"]["Shear_Stress"]])

mgs_fit10per = fitting([datafiles_mgs["MGS_w10per_mixed_3kPa"]["Normal_Stress"],
                        datafiles_mgs["MGS_w10per_mixed_6kPa"]["Normal_Stress"],
                        datafiles_mgs["MGS_w10per_mixed_9kPa"]["Normal_Stress"]],
                       [datafiles_mgs["MGS_w10per_mixed_3kPa"]["Shear_Stress"],
                        datafiles_mgs["MGS_w10per_mixed_6kPa"]["Shear_Stress"],
                        datafiles_mgs["MGS_w10per_mixed_9kPa"]["Shear_Stress"]])

mgs_fit20per = fitting([datafiles_mgs["MGS_w20per_mixed_3kPa"]["Normal_Stress"],
                        datafiles_mgs["MGS_w20per_mixed_6kPa"]["Normal_Stress"],
                        datafiles_mgs["MGS_w20per_mixed_9kPa"]["Normal_Stress"]],
                       [datafiles_mgs["MGS_w20per_mixed_3kPa"]["Shear_Stress"],
                        datafiles_mgs["MGS_w20per_mixed_6kPa"]["Shear_Stress"],
                        datafiles_mgs["MGS_w20per_mixed_9kPa"]["Shear_Stress"]])


jsc_fit0per = fitting([datafiles_jsc["JSC_w0per_dried_3kPa"]["Normal_Stress"],
                       datafiles_jsc["JSC_w0per_dried_6kPa"]["Normal_Stress"],
                       datafiles_jsc["JSC_w0per_dried_9kPa"]["Normal_Stress"]],
                      [datafiles_jsc["JSC_w0per_dried_3kPa"]["Shear_Stress"],
                       datafiles_jsc["JSC_w0per_dried_6kPa"]["Shear_Stress"],
                       datafiles_jsc["JSC_w0per_dried_9kPa"]["Shear_Stress"]])
jsc_fit10per = fitting([datafiles_jsc["JSC_w10per_mixed_3kPa"]["Normal_Stress"],
                        datafiles_jsc["JSC_w10per_mixed_6kPa"]["Normal_Stress"],
                        datafiles_jsc["JSC_w10per_mixed_9kPa"]["Normal_Stress"]],
                       [datafiles_jsc["JSC_w10per_mixed_3kPa"]["Shear_Stress"],
                        datafiles_jsc["JSC_w10per_mixed_6kPa"]["Shear_Stress"],
                        datafiles_jsc["JSC_w10per_mixed_9kPa"]["Shear_Stress"]])
jsc_fit20per = fitting([datafiles_jsc["JSC_w20per_mixed_3kPa"]["Normal_Stress"],
                        datafiles_jsc["JSC_w20per_mixed_6kPa"]["Normal_Stress"],
                        datafiles_jsc["JSC_w20per_mixed_9kPa"]["Normal_Stress"]],
                       [datafiles_jsc["JSC_w20per_mixed_3kPa"]["Shear_Stress"],
                        datafiles_jsc["JSC_w20per_mixed_6kPa"]["Shear_Stress"],
                        datafiles_jsc["JSC_w20per_mixed_9kPa"]["Shear_Stress"]])


mgs_allfits = [mgs_fit0per, mgs_fit10per, mgs_fit20per]
jsc_allfits = [jsc_fit0per, jsc_fit10per, jsc_fit20per]

water_contents = ["0", "10", "20"]


div = 1000

viridis = plt.get_cmap('viridis', len(water_contents))
colors_all = [viridis(i) for i in range(len(water_contents))]

color_map = {wc: color for wc, color in zip(water_contents, colors_all)}
pressure_symbols = {"3kPa": "o", "6kPa": "^", "9kPa": "s"}

mgs_key_colors = {}
mgs_key_symbols = {}
for key in datafiles_mgs:
    wc = extract_water_content(key)
    pressure = extract_pressure(key)
    if wc in color_map:
        mgs_key_colors[key] = color_map[wc]
    else:
        mgs_key_colors[key] = 'black'
    if pressure in pressure_symbols:
        mgs_key_symbols[key] = pressure_symbols[pressure]
    else:
        mgs_key_symbols[key] = 'x'
        
jsc_key_colors = {}
jsc_key_symbols = {}
for key in datafiles_jsc:
    wc = extract_water_content(key)
    pressure = extract_pressure(key)
    if wc in color_map:
        jsc_key_colors[key] = color_map[wc]
    else:
        jsc_key_colors[key] = 'black'
    if pressure in pressure_symbols:
        jsc_key_symbols[key] = pressure_symbols[pressure]
    else:
        jsc_key_symbols[key] = 'x'
        
legend_elementsize = 10
bar_fontsize = 10

fig, ax = plt.subplots(2,1, sharex = True)

for key, data in datafiles_mgs.items():
    x = data["Normal_Stress"] / div
    y = data["Shear_Stress"] / div
    ax[0].plot(x,y, marker = mgs_key_symbols[key], 
               linestyle = 'None', color = mgs_key_colors[key])

for key, data in datafiles_jsc.items():
    x = data["Normal_Stress"] / div
    y = data["Shear_Stress"] / div
    ax[1].plot(x,y, marker = jsc_key_symbols[key], 
               linestyle = 'None', color = jsc_key_colors[key])
    
i = 0
for fits in mgs_allfits:
    x_list = np.linspace(0, 8.5, 200)
    y_values = linfunc(fits["m"], fits["n"], x_list)
    ax[0].plot(x_list, y_values, marker = 'None', color = colors_all[i])
    i += 1

i = 0
for fits in jsc_allfits:
    x_list = np.linspace(0, 8.5, 200)
    y_values = linfunc(fits["m"], fits["n"], x_list)
    ax[1].plot(x_list, y_values, marker = 'None', color = colors_all[i])
    i += 1
    
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=10, label='3 kPa'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=10, label='6 kPa'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=10, label='9 kPa'),
]

ax[0].legend(handles = legend_elements, loc = 'upper left',
             fontsize = 10, frameon = True, fancybox = True, shadow = True)

pos = ax[1].get_position()
bar_width = 0.03
bar_left = pos.x1 + 0.005
bar_ax = fig.add_axes([bar_left, pos.y0, bar_width, pos.height * 2.2])

n_seg = len(water_contents)
segment_height = 1 / n_seg

for i, (wc, color) in enumerate(zip(water_contents, colors_all)):
    y_bottom = i* segment_height
    y_top = (i+1) * segment_height
    
    rect = Rectangle((0, y_bottom), 1, segment_height, facecolor = color, edgecolor = 'black', linewidth = 0.5)
    bar_ax.add_patch(rect)
    
    bar_ax.text(1.2, y_bottom + segment_height / 2, f'{wc}', transform = bar_ax.transData, 
                verticalalignment = 'center', fontsize = bar_fontsize)
    
    bar_ax.set_xlim(0,1)
    bar_ax.set_ylim(0,1)
    bar_ax.set_xticks([])
    bar_ax.set_yticks([])
    bar_ax.text(0.5, 1.02, "$\mathcal{W}$", transform = bar_ax.transAxes,
                horizontalalignment = 'center', fontsize = bar_fontsize)
    
ax[0].set_ylabel(r"$\tau$ [kPa]")
ax[0].set_xlim(0,8.5)
ax[0].set_ylim(0,4)
ax[0].xaxis.set_major_locator(MultipleLocator(1))
ax[0].yaxis.set_major_locator(MultipleLocator(1))
ax[0].xaxis.set_minor_locator(MultipleLocator(0.2))
ax[0].yaxis.set_minor_locator(MultipleLocator(0.2))
ax[0].grid(which = 'major', linestyle = '-')
ax[0].grid(which = 'minor', linestyle = ':')

ax[1].set_xlabel(r"$\sigma$ [kPa]")
ax[1].set_ylabel(r"$\tau$ [kPa]")
ax[1].set_ylim(0,4)
ax[1].xaxis.set_major_locator(MultipleLocator(1))
ax[1].yaxis.set_major_locator(MultipleLocator(1))
ax[1].xaxis.set_minor_locator(MultipleLocator(0.2))
ax[1].yaxis.set_minor_locator(MultipleLocator(0.2))
ax[1].grid(which = 'major', linestyle = '-')
ax[1].grid(which = 'minor', linestyle = ':')


plt.savefig("Figures/overview_marssimulants.pdf", dpi = 300, bbox_inches = 'tight')
plt.close(fig)

results_markersize = 10

fig_res, ax_res = plt.subplots(2,1, sharex = True)
ax_res_s = ax_res[1].secondary_yaxis('right', functions = (mu_to_phi, phi_to_mu))

i = 0
for fits in mgs_allfits:
    ax_res[0].errorbar(float(water_contents[i]), fits["n"]*1000, yerr = fits["n_error"]*1000, 
                             linestyle = 'None', marker = 'o', markersize = results_markersize, 
                             color = 'tab:red', capsize = 5, ecolor = 'black')
    ax_res[1].errorbar(float(water_contents[i]), fits["m"], yerr = fits["m_error"],
                       linestyle = 'None', marker = 'o', markersize = results_markersize,
                       color = 'tab:red', capsize = 5, ecolor = 'black')
    i+=1
i = 0
for fits in jsc_allfits:
    ax_res[0].errorbar(float(water_contents[i]), fits["n"]*1000, yerr = fits["n_error"]*1000, 
                             linestyle = 'None', marker = 'o', markersize = results_markersize, 
                             color = 'tab:blue', capsize = 5, ecolor = 'black')
    ax_res[1].errorbar(float(water_contents[i]), fits["m"], yerr = fits["m_error"],
                       linestyle = 'None', marker = 'o', markersize = results_markersize,
                       color = 'tab:blue', capsize = 5, ecolor = 'black')
    i += 1
    
ax_res[0].set_ylabel(r"$\tau_c$ [Pa]")
ax_res[0].yaxis.set_major_locator(MultipleLocator(200))
ax_res[0].set_ylim(0,970)
ax_res[1].yaxis.set_major_locator(MultipleLocator(0.1))
ax_res[1].set_ylim(0.2,0.5)
ax_res[1].set_xlabel(r"$\mathcal{W}$")
ax_res[1].set_ylabel(r"$\mu$ [-]")
ax_res_s.tick_params(which = 'both', length = 0)
ax_res_s.set_ylabel(r"$\phi$ $[^\circ]$")

plt.savefig("Figures/results_marssimulants.pdf", dpi = 300, bbox_inches = 'tight')
plt.close(fig_res)