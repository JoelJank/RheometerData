import pandas as pd
import openpyxl
import numpy as np
import matplotlib.pyplot as plt

data = "H:/AG Parteli/Paris/Data/rawdata/Glass/9kPa_redo_watercontain/20251023PSC_big_modified.xlsx"
lower_boundary = 8500
upper_boundary = 9500

df = pd.read_excel(data,  sheet_name = "W25%", 
                   header = None,
                   names = ["No","Time","Gap","Normal Force","Normal Stress","Torque","Shear Stress", "Rotational Speed"],
                   skiprows=4).dropna()

mask = df.apply(lambda row: any(isinstance(x, str) for x in row), axis=1)
df = df[~mask].dropna().reset_index(drop=True)

jumps_where = np.array([0])

num_col = df["No"].values
jumps_where_list = np.add(np.where(np.abs(np.diff(num_col)) > 10)[0], 1)
jumps_where = np.append(jumps_where,jumps_where_list)
jumps_where = np.append(jumps_where, len(df))
sections = [df.iloc[jumps_where[i]:jumps_where[i+1]].reset_index(drop=True) for i in range(len(jumps_where)-1)]

filtered_sections = [
    section for section in sections
    if len(section) >= 25
    and not ((section["Normal Stress"] >= lower_boundary) & (section["Normal Stress"] <= upper_boundary)).any()
]

result_df = pd.concat(filtered_sections, ignore_index= True)

plt.plot(result_df["Time"]/60,result_df["Normal Stress"], color = "blue")
plt.plot(result_df["Time"]/60, result_df["Shear Stress"], color = "red")
plt.savefig("test.png", dpi=300)

result_df.to_excel("H:/AG Parteli/Paris/Data/rawdata/Glass/9kPa_redo_watercontain/W25%.xlsx", index = False)


