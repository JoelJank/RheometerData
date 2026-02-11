import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
from functools import reduce
import scipy.stats

plt.style.use('paper.mplstyle')

def flatten(l):
    return list(reduce(lambda x, y: x + y, l, []))


def read_file(filepath):
    df = pd.read_csv(filepath, delimiter = ';', header = None, skiprows=1, decimal = ".", names = ["Sheetname", "m","n", "y-intercept", "Angle", "Times_max", "ns","ss"])
    for col in ["Times_max", "ns","ss"]:
        df[col] = df[col].apply(lambda x: [float(i) for i in str(x).split(';') if i != ''])
        
    return df

def lin_fit(x, slope, intercept):
    return slope * x + intercept

def get_slope_intercept(data):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(sorted(flatten([data["ns"][0], data["ns"][1], data["ns"][2]])), sorted(flatten([data["ss"][0], data["ss"][1], data["ss"][2]])))#
    return [slope, intercept, r_value, p_value, std_err]

water10_data = read_file("H:\AG Parteli\Paris\Data\processed\JSC/10per_mixed\mohr_coulomb.csv")
water20_data = read_file("H:\AG Parteli\Paris\Data\processed\JSC/20per_mixed\mohr_coulomb.csv")
water0_data = read_file("H:\AG Parteli\Paris\Data\processed\JSC/dried\mohr_coulomb.csv")

x10_list = sorted(flatten([water10_data["ns"][0], water10_data["ns"][1], water10_data["ns"][2]]))
x20_list = sorted(flatten([water20_data["ns"][0], water20_data["ns"][1], water20_data["ns"][2]]))
x0_list = sorted(flatten([water0_data["ns"][0], water0_data["ns"][1], water0_data["ns"][2]]))

x10 = np.linspace(0, x10_list[-1],1000)
x20 = np.linspace(0, x20_list[-1],1000)
x0 = np.linspace(0, x0_list[-1],1000)


x0_plot_0 = plt.plot(water0_data["ns"][0], water0_data["ss"][0], 'o', color = "#323333", linestyle = "None")
x0_plot_1 = plt.plot(water0_data["ns"][1], water0_data["ss"][1], 'v', color = x0_plot_0[0].get_color(), linestyle = "None")
x0_plot_2 = plt.plot(water0_data["ns"][2], water0_data["ss"][2], 'h', color = x0_plot_0[0].get_color(), linestyle = "None")
x0_fit = plt.plot(x0, lin_fit(x0, *get_slope_intercept(water0_data)[:2]), linestyle = '-', color = x0_plot_0[0].get_color(), label = 'dried')

x10_plot_0 = plt.plot(water10_data["ns"][0], water10_data["ss"][0], 'o', color = "#1f77b4", linestyle = "None")
x10_plot_1 = plt.plot(water10_data["ns"][1], water10_data["ss"][1], 'v', color = x10_plot_0[0].get_color(), linestyle = "None")
x10_plot_2 = plt.plot(water10_data["ns"][2], water10_data["ss"][2], 'h', color = x10_plot_0[0].get_color(), linestyle = "None")
x10_fit = plt.plot(x10, lin_fit(x10, *get_slope_intercept(water10_data)[:2]), linestyle = '-', color = x10_plot_0[0].get_color(), label = '10% water')

x20_plot_0 = plt.plot(water20_data["ns"][0], water20_data["ss"][0], 'o', color = "#ff7f0e", linestyle = "None")
x20_plot_1 = plt.plot(water20_data["ns"][1], water20_data["ss"][1], 'v', color = x20_plot_0[0].get_color(), linestyle = "None")
x20_plot_2 = plt.plot(water20_data["ns"][2], water20_data["ss"][2], 'h', color = x20_plot_0[0].get_color(), linestyle = "None")
x20_fit = plt.plot(x20, lin_fit(x20, *get_slope_intercept(water20_data)[:2]), linestyle = '-', color = x20_plot_0[0].get_color(), label = '20% water')

fit_legend = plt.legend(loc='upper left')
plt.gca().add_artist(fit_legend)
# Custom legend for symbols/pressure
custom_lines = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#323333', markersize=8, label='5 kPa'),
    Line2D([0], [0], marker='v', color='w', markerfacecolor='#323333', markersize=8, label='10 kPa'),
    Line2D([0], [0], marker='h', color='w', markerfacecolor='#323333', markersize=8, label='15 kPa'),
]
plt.legend(handles=custom_lines, title='Preshear consolidation pressure', loc='lower right')
plt.xlabel("Normal Stress (Pa)")
plt.ylabel("Shear Stress (Pa)")
plt.savefig("JSC.svg", dpi = 300)
