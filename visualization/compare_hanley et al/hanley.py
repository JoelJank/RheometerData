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

hanley_data = pd.read_csv("Hanley_data/dryglass.csv", header = None, names = ["ns","ss"], sep = ";")

water2_5_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\9kPa_redo\W2.5\mohr_coulomb.csv")
water5_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\9kPa_redo\W5_2\mohr_coulomb.csv")
water7_5_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\9kPa_redo\W7.5\mohr_coulomb.csv")
water10_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass/10per_unmixed\mohr_coulomb.csv")
water10_data = water10_data.tail(1).reset_index(drop=True)
water12_5_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\9kPa_redo\W12.5\mohr_coulomb.csv")
water17_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\9kPa_redo\W17_2\mohr_coulomb.csv")
water20_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass/20per_mixed\mohr_coulomb.csv")
water20_data = water20_data.tail(1).reset_index(drop=True)
water22_5_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\9kPa_redo\W22.5\mohr_coulomb.csv")
water25_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\9kPa_redo\W25_2\mohr_coulomb.csv")
water0_data = read_file("H:\AG Parteli\Paris\Data\processed\Glass\dried\mohr_coulomb.csv")
water0_data = water0_data.iloc[[-2]].reset_index(drop=True)
highnormal_dried = read_file("H:\AG Parteli\Paris\Data\processed\Glass\dried\mohr_coulomb.csv")
highnormal_dried = highnormal_dried.tail(1).reset_index(drop=True)
highnormal_water5 = read_file("H:\AG Parteli\Paris\Data\processed\Glass/15kPa/5per/mohr_coulomb.csv")
highnormal_water15 = read_file("H:\AG Parteli\Paris\Data\processed\Glass/15kPa/15per/mohr_coulomb.csv")
highnormal_water25 = read_file("H:\AG Parteli\Paris\Data\processed\Glass/15kPa/25per/mohr_coulomb.csv")


#First plot: all files without high normal stress with linear fits

x = np.linspace(0, sorted(flatten([water0_data["ns"][0], water2_5_data["ns"][0], water5_data["ns"][0], water7_5_data["ns"][0], water10_data["ns"][0], water12_5_data["ns"][0], water17_data["ns"][0], water20_data["ns"][0], water22_5_data["ns"][0], water25_data["ns"][0]]))[-1],1000)

def lin_fit(x, slope, intercept):
    return slope * x + intercept

def get_slope_intercept(data):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(data["ns"][0], data["ss"][0])#
    return [slope, intercept, r_value, p_value, std_err]

print(round(get_slope_intercept(water2_5_data)[2],5))

dried = plt.plot(water0_data["ns"][0], water0_data["ss"][0], 'o', label='dried', color = "#323333", linestyle = "None")
dried_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water0_data)[:2]), linestyle = '-', color = dried[0].get_color())
# Use a color gradient from blue to red for water content
w2_5 = plt.plot(water2_5_data["ns"][0], water2_5_data["ss"][0], 'v', label='2.5% water', color = "#4575b4", linestyle = "None")
w2_5_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water2_5_data)[:2]), linestyle = '-', color = w2_5[0].get_color())
w5 = plt.plot(water5_data["ns"][0], water5_data["ss"][0], 's', label='5% water', color = "#91bfdb", linestyle = "None")
w5_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water5_data)[:2]), linestyle = '-', color = w5[0].get_color())
w7_5 = plt.plot(water7_5_data["ns"][0], water7_5_data["ss"][0], 'D', label='7.5% water', color = "#e0f3f8", linestyle = "None")
w7_5_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water7_5_data)[:2]), linestyle = '-', color = w7_5[0].get_color())
w10 = plt.plot(water10_data["ns"][0], water10_data["ss"][0], '^', label='10% water', color = "#ffffbf", linestyle = "None")
w10_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water10_data)[:2]), linestyle = '-', color = w10[0].get_color())
w12_5 = plt.plot(water12_5_data["ns"][0], water12_5_data["ss"][0], 'P', label='12.5% water', color = "#fee090", linestyle = "None")
w12_5_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water12_5_data)[:2]), linestyle = '-', color = w12_5[0].get_color())
w17 = plt.plot(water17_data["ns"][0], water17_data["ss"][0], 'X', label='17% water', color = "#fc8d59", linestyle = "None")
w17_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water17_data)[:2]), linestyle = '-', color = w17[0].get_color())
w20 = plt.plot(water20_data["ns"][0], water20_data["ss"][0], '*', label='20% water', color = "#d73027", linestyle = "None")
w20_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water20_data)[:2]), linestyle = '-', color = w20[0].get_color())
w22_5 = plt.plot(water22_5_data["ns"][0], water22_5_data["ss"][0], 'H', label='22.5% water', color = "#7f0000", linestyle = "None")
w22_5_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water22_5_data)[:2]), linestyle = '-', color = w22_5[0].get_color())
"""
w25 = plt.plot(water25_data["ns"][0], water25_data["ss"][0], '8', label='25% water', color = "#4B6E8E", linestyle = "None")
w25_fit = plt.plot(x, lin_fit(x, *get_slope_intercept(water25_data)[:2]), linestyle = '-', label=f'25% water fit, $R^2 = {round(get_slope_intercept(water25_data)[2],5)}$', color = w25[0].get_color())
"""
plt.legend(loc = 'upper left', fontsize = 8)
plt.xlabel("Normal Stress(Pa)")
plt.ylabel("Shear Stress(Pa)")
plt.savefig("newglassdata.svg", dpi = 300)


#Hanley compare
#todo

