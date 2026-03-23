import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = "H:\\AG Parteli\\Paris\\Github\\RheometerData\\Data\\Glass\\90 micron\\smallcup\\w0per_3_6_15_kPa\\w0per_3_6_15_kPa.xlsx"
lower_boundary = 14800
upper_boundary = 15300

df = pd.read_excel(data,  sheet_name = "15kPa", 
                   header = None,
                   names = ["No","Time","Gap","Normal Force","Normal Stress","Torque","Shear Stress", "Rotational Speed"],
                   skiprows=2).dropna()


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
    if len(section) >= 41
    and not ((section["Normal Stress"] >= lower_boundary) & (section["Normal Stress"] <= upper_boundary)).any()
]

result_df = pd.concat(filtered_sections, ignore_index= True)

plt.plot(result_df["Time"]/60,result_df["Normal Stress"], color = "blue")
plt.plot(result_df["Time"]/60, result_df["Shear Stress"], color = "red")
plt.savefig("test.png", dpi=300)

result_df.to_excel("H:\\AG Parteli\\Paris\\Github\\RheometerData\\Data\\Glass\\90 micron\\smallcup\\w0per_3_6_15_kPa\\15kPa.xlsx", index = False)


