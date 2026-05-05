from Functions.functions import read_data, split_dataframe, fitting, linfunc, extract_water_content, extract_pressure, mu_to_phi, phi_to_mu
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.lines import Line2D
import os
import numpy as np
import pandas as pd
from scipy import optimize
plt.style.use('computermodernstyle.mplstyle')


original_9kPa = ["../Data/Glass/420 micron/9kPa/w0per_dried/mohr_coulomb.csv",
                "../Data/Glass/420 micron/9kPa/w10per_mixed/mohr_coulomb.csv",
                "../Data/Glass/420 micron/9kPa/w20per_mixed/mohr_coulomb.csv"]

original_15kPa = ["../Data/Glass/420 micron/15kPa/w0per_dried/mohr_coulomb.csv",
                  "../Data/Glass/420 micron/15kPa/w5per_unmixed/mohr_coulomb.csv",
                  "../Data/Glass/420 micron/15kPa/w15per_unmixed/mohr_coulomb.csv",
                  "../Data/Glass/420 micron/15kPa/w25per_unmixed/mohr_coulomb.csv"]

redo_9kPa = ["../Data/Glass/420 micron/9kPa/w2.5per_unmixed/mohr_coulomb.csv",
             "../Data/Glass/420 micron/9kPa/w5per_unmixed/mohr_coulomb.csv",
             "../Data/Glass/420 micron/9kPa/w7.5per_unmixed/mohr_coulomb.csv",
             "../Data/Glass/420 micron/9kPa/w12.5per_unmixed/mohr_coulomb.csv",
             "../Data/Glass/420 micron/9kPa/w17per_unmixed/mohr_coulomb.csv",
             "../Data/Glass/420 micron/9kPa/w22.5per_unmixed/mohr_coulomb.csv",
             "../Data/Glass/420 micron/9kPa/w25per_unmixed/mohr_coulomb.csv"] 

datafiles = {}

for filepath in original_15kPa + redo_9kPa:
    parts = os.path.normpath(filepath).split(os.sep)
    name = f"{parts[-3]}_{parts[-2]}"
    data = read_data(filepath)
    datafiles[name] = data
    
for filepath in original_9kPa:
    parts = os.path.normpath(filepath).split(os.sep)
    name = f"{parts[-3]}_{parts[-2]}"
    data = read_data(filepath)
    data_split = split_dataframe(data, name)
    datafiles.update(data_split)
    


fit0per = fitting([datafiles['9kPa_w0per_dried_3kPa']["Normal_Stress"],
                   datafiles['9kPa_w0per_dried_6kPa']["Normal_Stress"],
                   datafiles['9kPa_w0per_dried_9kPa']["Normal_Stress"],
                   datafiles['15kPa_w0per_dried']["Normal_Stress"][0:3]
                   ],
                  [datafiles['9kPa_w0per_dried_3kPa']["Shear_Stress"],
                   datafiles['9kPa_w0per_dried_6kPa']["Shear_Stress"],
                   datafiles['9kPa_w0per_dried_9kPa']["Shear_Stress"],
                   datafiles['15kPa_w0per_dried']["Shear_Stress"][0:3]
                   ])

fit2_5per = fitting([datafiles['9kPa_w2.5per_unmixed']["Normal_Stress"]],
                    [datafiles['9kPa_w2.5per_unmixed']["Shear_Stress"]])

fit5per = fitting([datafiles['15kPa_w5per_unmixed']["Normal_Stress"][0:3],
                   datafiles['9kPa_w5per_unmixed']["Normal_Stress"]],
                  [datafiles['15kPa_w5per_unmixed']["Shear_Stress"][0:3],
                   datafiles['9kPa_w5per_unmixed']["Shear_Stress"]])

fit7_5per = fitting([datafiles['9kPa_w7.5per_unmixed']["Normal_Stress"]],
                    [datafiles['9kPa_w7.5per_unmixed']["Shear_Stress"]])

fit10per = fitting([datafiles['9kPa_w10per_mixed_3kPa']["Normal_Stress"],
                    datafiles['9kPa_w10per_mixed_6kPa']["Normal_Stress"]],
                   [datafiles['9kPa_w10per_mixed_3kPa']["Shear_Stress"],
                    datafiles['9kPa_w10per_mixed_6kPa']["Shear_Stress"]])

fit12_5per = fitting([datafiles['9kPa_w12.5per_unmixed']["Normal_Stress"]],
                     [datafiles['9kPa_w12.5per_unmixed']["Shear_Stress"]])

fit15per = fitting([datafiles['15kPa_w15per_unmixed']["Normal_Stress"][0:3]],
                    [datafiles['15kPa_w15per_unmixed']["Shear_Stress"][0:3]])

fit17per = fitting([datafiles['9kPa_w17per_unmixed']["Normal_Stress"]],
                    [datafiles['9kPa_w17per_unmixed']["Shear_Stress"]])

fit20per = fitting([datafiles['9kPa_w20per_mixed_3kPa']["Normal_Stress"],
                    datafiles['9kPa_w20per_mixed_6kPa']["Normal_Stress"],
                    datafiles['9kPa_w20per_mixed_9kPa']["Normal_Stress"]],
                    [datafiles['9kPa_w20per_mixed_3kPa']["Shear_Stress"],
                     datafiles['9kPa_w20per_mixed_6kPa']["Shear_Stress"],
                     datafiles['9kPa_w20per_mixed_9kPa']["Shear_Stress"]],
                   )

fit22_5per = fitting([datafiles['9kPa_w22.5per_unmixed']["Normal_Stress"]],
                     [datafiles['9kPa_w22.5per_unmixed']["Shear_Stress"]])

fit25per = fitting([datafiles['15kPa_w25per_unmixed']["Normal_Stress"][0:3],
                    datafiles['9kPa_w25per_unmixed']["Normal_Stress"]],
                   [datafiles['15kPa_w25per_unmixed']["Shear_Stress"][0:3],
                    datafiles['9kPa_w25per_unmixed']["Shear_Stress"]])

all_fits = [fit0per, fit2_5per, fit5per, fit7_5per, fit10per, fit12_5per, fit15per, fit17per, fit20per, fit22_5per, fit25per]
keys = sorted(list(datafiles.keys()))
water_contents = ["0", "2.5", "5", "7.5", "10", "12.5", "15", "17", "20", "22.5", "25"]

viridis = plt.get_cmap('viridis', len(water_contents))

colors_all = [viridis(i) for i in range(len(water_contents))]
color_map = {wc: color for wc, color in zip(water_contents, colors_all)}

pressure_symbols = {"3kPa": "o", "6kPa": "^", "9kPa": "s", "15kPa": "p"}

key_colors = {}
key_symbols = {}
for key in datafiles:
    wc = extract_water_content(key)
    pressure = extract_pressure(key)
    if wc in color_map:
        key_colors[key] = color_map[wc]
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

#Figure for glass overview

fig, ax1 = plt.subplots()

ax_inset = inset_axes(ax1, width = '50%', height = '40%', 
                      loc = 'upper left', bbox_to_anchor = (0.08, -0.04, 0.96, 0.96),
                      bbox_transform = ax1.transAxes, borderpad = 1)

for key, data in datafiles.items():
    x = data["Normal_Stress"] / div
    y = data["Shear_Stress"] / div
    
    ax1.plot(x,y, marker = key_symbols[key], linestyle = 'None', color = key_colors[key])
    ax_inset.plot(x,y, marker = key_symbols[key], linestyle = 'None', color = key_colors[key],
                  markeredgecolor = 'black', markersize = inset_markers)
i = 0
for fits in all_fits:
    x_list = np.linspace(0,8.5,200)
    y_values = linfunc(fits['m'], fits['n'], x_list)
    ax_inset.plot(x_list, y_values, color = colors_all[i], marker = 'None')
    i += 1
    
rect = Rectangle((-0.15, -0.24,), 1.3, 1.48,
                 transform = ax_inset.transAxes,
                 facecolor = 'white',
                 edgecolor = 'black',
                 linewidth = 0,
                 zorder = -2,
                 clip_on = False
                 )

ax_inset.add_patch(rect)

ax_inset.set_xlabel(r'$\sigma$ [kPa]', size = inset_labelsize)
ax_inset.set_ylabel(r'$\tau$ [kPa]', size = inset_labelsize)
ax_inset.set_xlim(0,8)
ax_inset.set_ylim(0,2.5)
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

legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=legend_elementsize, label='3 kPa'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=legend_elementsize, label='6 kPa'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=legend_elementsize, label='9 kPa'),
    Line2D([0], [0], marker='p', color='w', markerfacecolor='gray', markeredgecolor='black', 
           markersize=legend_elementsize, label='15 kPa')
]

ax1.legend(handles = legend_elements, loc = 'upper right', fontsize = 10, 
           frameon = True, fancybox = True, shadow = True)

ax1.set_xlabel(r'$\sigma$ [kPa]')
ax1.set_ylabel(r'$\tau$ [kPa]')
ax1.xaxis.set_major_locator(MultipleLocator(1))
ax1.yaxis.set_major_locator(MultipleLocator(1))
ax1.xaxis.set_minor_locator(MultipleLocator(0.2))
ax1.yaxis.set_minor_locator(MultipleLocator(0.2))
ax1.grid(which = 'major', linestyle = '-')
ax1.grid(which = 'minor', linestyle = ':')
ax1.set_xlim(0,13)
ax1.set_ylim(0,7.2)

pos = ax1.get_position()
bar_width = 0.03
bar_left = pos.x1 + 0.005
bar_ax = fig.add_axes([bar_left, pos.y0, bar_width, pos.height])

n_seg = len(water_contents)
segment_height = 1 / n_seg

for i, (wc, color) in enumerate(zip(water_contents, colors_all)):
    y_bottom = i * segment_height
    y_top = (i+1) * segment_height
    
    rect = Rectangle((0,y_bottom), 1, segment_height, facecolor = color, edgecolor = 'black', linewidth = 0.5)
    bar_ax.add_patch(rect)
    bar_ax.text(1.2, y_bottom + segment_height / 2, f'{wc}', transform = bar_ax.transData, 
                verticalalignment = 'center', fontsize = bar_fontsize)
    bar_ax.set_xlim(0, 1)
    bar_ax.set_ylim(0, 1)
    bar_ax.set_xticks([])
    bar_ax.set_yticks([])
    bar_ax.text(0.5, 1.02, "$\mathcal{W}$", transform = bar_ax.transAxes,
                horizontalalignment = 'center', fontsize = bar_fontsize)


plt.savefig("Figures/glass_overview.pdf", dpi=300, bbox_inches = 'tight')
plt.close(fig)


# Figure for Water against tau_c and phi


def expfitfunc(x, tau_c_infty, c, b):
    y = tau_c_infty*(1-c*np.exp(-b*x))
    return y

richefeu = pd.read_csv("RIchefeu_data/richefeu.csv", sep = ";", header = None, decimal = ",")

results_markersize = 10

fig, ax2 = plt.subplots(2,1, sharex = True)

fit_data_w = []
fit_data_tau = []
fit_data_err = []

i = 0

for fit in all_fits:
    m_val = float(water_contents[i])
    mu = fit["m"]
    mu_error = fit["m_error"]
    
    ax2[0].errorbar(m_val, fit["n"]*1000, yerr = fit["n_error"]*1000, linestyle = 'None',
                    marker = 'o', markersize = results_markersize, color = 'tab:red',
                    capsize = 5, ecolor = 'black', label = 'Present' if i == 0 else "")
    
    ax2[1].errorbar(m_val, mu, yerr = mu_error, linestyle = 'None', marker = 'o',
                    markersize = results_markersize, color = 'tab:red', capsize = 5, ecolor = 'black')
    
    fit_data_w.append(m_val)
    fit_data_tau.append(fit["n"]*1000)
    fit_data_err.append(fit["n_error"]*1000)
    i += 1
    
initial_guess = [max(fit_data_tau), 0.9, 0.1]

exp_fit, exp_cov = optimize.curve_fit(expfitfunc, fit_data_w, fit_data_tau, 
                                                p0 = initial_guess, sigma = fit_data_err, absolute_sigma = True)

w_smooth = np.linspace(min(fit_data_w), max(fit_data_w), 100)
tau_fitted = expfitfunc(w_smooth, *exp_fit)

ax2[0].plot(w_smooth, tau_fitted, linestyle = '--', color = 'gray')
ax2[0].plot(richefeu[0]*100, richefeu[1], linestyle='None', marker='o', 
            markeredgecolor='tab:blue', markerfacecolor = 'none', markeredgewidth = 1.5, 
            markersize = 10, label = 'Richefeu et al. 2006')

ax2[0].set_ylabel(r"$\tau_c$ [Pa]")
ax2[0].set_ylim(0, 850)
ax2[0].yaxis.set_major_locator(MultipleLocator(200))
ax2[0].legend(loc = 'best', fontsize = 10, frameon = True, fancybox = True, shadow = False)
ax2[1].set_xlabel(r'$\mathcal{W}$')
ax2[1].set_ylabel(r'$\mu$ [-]')

ax2s = ax2[1].secondary_yaxis('right', functions = (mu_to_phi, phi_to_mu))
ax2s.set_ylabel(r'$\phi$ [$^{\circ}$]')
ax2s.tick_params(which = 'both', length = 0)

tau_c_infty_fit, c_fit, b_fit = exp_fit
param_errors = np.sqrt(np.diag(exp_cov))

residuals = np.array(fit_data_tau) - expfitfunc(np.array(fit_data_w), *exp_fit)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((np.array(fit_data_tau) - np.mean(fit_data_tau))**2)
r_squared = 1 - (ss_res / ss_tot)

print(f"τ_c∞     = {tau_c_infty_fit:.2f} ± {param_errors[0]:.2f} kPa")
print(f"c        = {c_fit:.4f} ± {param_errors[1]:.4f}")
print(f"b        = {b_fit:.4f} ± {param_errors[2]:.4f}")
print(f"R²       = {r_squared:.4f}")

plt.savefig("Figures/glass_results.pdf", dpi = 300, bbox_inches = 'tight')





