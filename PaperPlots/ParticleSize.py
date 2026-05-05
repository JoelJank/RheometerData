import numpy as np
import matplotlib.pyplot as plt
from Functions.functions import read_data, split_dataframe, fitting, linfunc, extract_particlediameter, extract_pressure, mu_to_phi, phi_to_mu
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
plt.style.use('computermodernstyle.mplstyle')

datafiles_90micron = ["../Data/Glass/90 micron/bigcup/w0per_3_6_15_kPa/mohr_coulomb.csv"]
datafiles_230micron_A = ["../Data/Glass/230 micron/bigcup/w0per_3_6_15_kPa/A/mohr_coulomb.csv"]
datafiles_230micron_B = ["../Data/Glass/230 micron/bigcup/w0per_3_6_15_kPa/B/mohr_coulomb.csv"]
datafiles_420micron_9kPa = ["../Data/Glass/420 micron/9kPa/w0per_dried/mohr_coulomb.csv"]

datafiles = {}

for filepath in datafiles_90micron + datafiles_230micron_A + datafiles_230micron_B + datafiles_420micron_9kPa:
    parts = os.path.normpath(filepath).split(os.sep)
    name = f"{parts[-4]}_{parts[-3]}_{parts[-2]}"
    if filepath in datafiles_230micron_A or filepath in datafiles_230micron_B:
        name = f"{parts[-5]}_{parts[-3]}_{parts[-2]}"
    data = read_data(filepath)
    data_split = split_dataframe(data,name)
    datafiles.update(data_split)
    

fit420micron = fitting([datafiles["420 micron_9kPa_w0per_dried_3kPa"]["Normal_Stress"],
                        datafiles["420 micron_9kPa_w0per_dried_6kPa"]["Normal_Stress"],
                        datafiles["420 micron_9kPa_w0per_dried_9kPa"]["Normal_Stress"],
                        datafiles["420 micron_9kPa_w0per_dried_15kPa"]["Normal_Stress"][0:3]],
                       [datafiles["420 micron_9kPa_w0per_dried_3kPa"]["Shear_Stress"],
                        datafiles["420 micron_9kPa_w0per_dried_6kPa"]["Shear_Stress"],
                        datafiles["420 micron_9kPa_w0per_dried_9kPa"]["Shear_Stress"],
                        datafiles["420 micron_9kPa_w0per_dried_15kPa"]["Shear_Stress"][0:3]])

fit230micron = fitting([datafiles["230 micron_w0per_3_6_15_kPa_A_3kPa"]["Normal_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_A_6kPa"]["Normal_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_A_15kPa"]["Normal_Stress"][0:2],
                         datafiles["230 micron_w0per_3_6_15_kPa_B_3kPa"]["Normal_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_B_6kPa"]["Normal_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_B_15kPa"]["Normal_Stress"][0:2]],
                        [datafiles["230 micron_w0per_3_6_15_kPa_A_3kPa"]["Shear_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_A_6kPa"]["Shear_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_A_15kPa"]["Shear_Stress"][0:2],
                         datafiles["230 micron_w0per_3_6_15_kPa_B_3kPa"]["Shear_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_B_6kPa"]["Shear_Stress"],
                         datafiles["230 micron_w0per_3_6_15_kPa_B_15kPa"]["Shear_Stress"][0:2]])

fit90micron = fitting([datafiles["90 micron_bigcup_w0per_3_6_15_kPa_3kPa"]["Normal_Stress"],
                       datafiles["90 micron_bigcup_w0per_3_6_15_kPa_6kPa"]["Normal_Stress"],
                       datafiles["90 micron_bigcup_w0per_3_6_15_kPa_15kPa"]["Normal_Stress"][0:2]],
                      [datafiles["90 micron_bigcup_w0per_3_6_15_kPa_3kPa"]["Shear_Stress"],
                       datafiles["90 micron_bigcup_w0per_3_6_15_kPa_6kPa"]["Shear_Stress"],
                       datafiles["90 micron_bigcup_w0per_3_6_15_kPa_15kPa"]["Shear_Stress"][0:2]])

all_fits = [fit90micron, fit230micron, fit420micron]

particle_sizes = ["90 micron", "230 micron", "420 micron"]
sizes = [r'90 - 106', r'230 - 300', r'400 - 450']
viridis = plt.get_cmap('viridis', len(particle_sizes))
colors_all = [viridis(i) for i in range(len(particle_sizes))]

color_map = {wc: color for wc, color in zip(particle_sizes, colors_all)}
pressure_symbols = {"3kPa": "o", "6kPa": "^", "9kPa": "s", "15kPa": "p"}

key_colors = {}
key_symbols = {}

for key in datafiles:
    particle_diameter = extract_particlediameter(key)
    pressure = extract_pressure(key)
    
    if particle_diameter in color_map:
        key_colors[key] = color_map[particle_diameter]
    else:
        key_colors[key] = 'black'
    
    if pressure in pressure_symbols:
        key_symbols[key] = pressure_symbols[pressure]
    else:
        key_symbols[key] = 'x'

div = 1000
inset_markers = 6
inset_labelsize = 10
inset_ticksize = 8
legend_elementsize = 10
bar_fontsize =13

fig, ax1 = plt.subplots()

ax_inset = inset_axes(ax1, width = "50 %", height = "40%", loc = 'upper left',
                      bbox_to_anchor = (0.08, -0.04, 0.96, 0.96), 
                      bbox_transform = ax1.transAxes, borderpad = 1)

rect = Rectangle(
    (-0.15, -0.24), 1.3, 1.48, 
    transform=ax_inset.transAxes, 
    facecolor='white', 
    edgecolor='black', 
    linewidth=0,
    zorder=-1,
    clip_on=False
)
ax_inset.add_patch(rect)

for key, data in datafiles.items():
    x_array = data["Normal_Stress"] / div
    y_array = data["Shear_Stress"] / div
    ax1.plot(x_array, y_array, marker = key_symbols[key], linestyle = 'none', markeredgecolor = 'black',
             color = key_colors[key])
    ax_inset.plot(x_array, y_array, marker = key_symbols[key], linestyle = 'none', markeredgecolor = 'black',
             color = key_colors[key], markersize = inset_markers)
    

pos = ax1.get_position()
bar_width = 0.03
bar_left = pos.x1 + 0.005
bar_ax = fig.add_axes([bar_left, pos.y0, bar_width, pos.height])
n_seg = len(particle_sizes)
segment_height = 1/n_seg

for i, (wc, color) in enumerate(zip(sizes, colors_all)):
    y_bottom = i * segment_height
    y_top = (i + 1) * segment_height
    
    rect = Rectangle((0, y_bottom), 1, segment_height, facecolor = color, edgecolor = 'black', linewidth = 0.5)
    bar_ax.add_patch(rect)
    
    bar_ax.text(1.2, y_bottom + segment_height / 2, f'{wc}', 
                transform = bar_ax.transData, va = 'center', fontsize = bar_fontsize)
    bar_ax.set_xlim(0,1)
    bar_ax.set_ylim(0,1)
    bar_ax.set_xticks([])
    bar_ax.set_yticks([])
    bar_ax.text(0.5, 1.02, 'Particle \n Diameter \n [$\mu m$]', transform = bar_ax.transAxes,
                ha = 'center', fontsize = bar_fontsize)
    
i = 0

for fit in all_fits:
    x_list = np.linspace(0, 8.5, 200)
    y_values = linfunc(fit["m"], fit["n"], x_list)
    ax_inset.plot(x_list, y_values, color = colors_all[i], linestyle = '-', label = sizes[i])
    i += 1
    
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=10, label='3 kPa'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=10, label='6 kPa'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=10, label='9 kPa'),
    Line2D([0], [0], marker='p', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=10, label='15 kPa')
]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=10, frameon=True, fancybox=True, shadow=True)

ax1.set_xlabel(r'$\sigma$ [kPa]')
ax1.set_ylabel(r'$\tau$ [kPa]')
ax1.xaxis.set_major_locator(MultipleLocator(1))
ax1.yaxis.set_major_locator(MultipleLocator(1))
ax1.xaxis.set_minor_locator(MultipleLocator(0.2))
ax1.yaxis.set_minor_locator(MultipleLocator(0.2))
ax1.grid(which = 'major', linestyle = '-')
ax1.grid(which = 'minor', linestyle = ':')
ax1.set_xlim(0,13)
ax1.set_ylim(0,6)

ax_inset.set_xlabel(r'$\sigma$ [kPa]', size = inset_labelsize)
ax_inset.set_ylabel(r'$\tau$ [kPa]', size = inset_labelsize)
ax_inset.set_xlim(0,8.1)
ax_inset.set_ylim(0,2)
ax_inset.tick_params(labelsize = inset_ticksize)
ax_inset.tick_params(axis = 'x', which = 'both', top = True, 
                     bottom = True, direction = 'in', labelbottom = True)
ax_inset.tick_params(axis = 'y', which = 'both', left = True, 
                     right = True, direction = 'in', labelleft = True)
ax_inset.xaxis.set_major_locator(MultipleLocator(1))
ax_inset.yaxis.set_major_locator(MultipleLocator(1))
ax_inset.xaxis.set_minor_locator(MultipleLocator(0.2))
ax_inset.yaxis.set_minor_locator(MultipleLocator(0.2))
ax_inset.grid(which = 'major', linestyle = '-')
ax_inset.grid(which = 'minor', linestyle = ':')


    
plt.savefig("Figures/particlesizes.pdf", dpi = 300, bbox_inches = 'tight')