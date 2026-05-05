import pandas as pd
import numpy as np
from scipy import optimize


def read_data(file):
    df = pd.read_csv(file, sep = ';')

    all_data = []

    for idf, row in df.iterrows():
        sheet_name = row['Sheetname']

        normal_stress_str = row['Normal Stress']
        shear_stress_str = row['Shear Stress max']

        normal_stress_values = [float(x.strip()) for x in normal_stress_str.split(';')]
        shear_stress_values = [float(x.strip()) for x in shear_stress_str.split(';')]

        for i, (n,s) in enumerate(zip(normal_stress_values, shear_stress_values)):
            data_point = {
                'Sheetname': sheet_name,
                'm': row['m'],
                'y-intercept': row['y-intercept'],
                'Angle': row['Angle'],
                'Times_max': row['Times_max'].split(';')[i] if ';' in str(row['Times_max']) else row['Times_max'],
                'Normal_Stress': n,
                'Shear_Stress': s,
            }
            all_data.append(data_point)

        result_df = pd.DataFrame(all_data)

        numeric_columns = ['m', 'y-intercept', 'Angle', 'Normal_Stress', 'Shear_Stress']
        for col in numeric_columns:
            if col in result_df.columns:
                result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
    
    return result_df


def split_dataframe(df, name):

    result_dict = {}
    
    for sheetname in df['Sheetname'].unique():
        filtered_df = df[df['Sheetname'] == sheetname].copy()
        filtered_df.reset_index(drop=True, inplace=True)
        dictname = f"{name}_{sheetname}"
        result_dict[dictname] = filtered_df
    return result_dict



def fitting(x_data,y_data):

    x_combined = []
    y_combined = []


    for x_list, y_list in zip(x_data, y_data):
        x_combined.extend(x_list)
        y_combined.extend(y_list)

    data_pairs = list(zip(x_combined, y_combined))
    data_pairs.sort(key=lambda pair: pair[0])

    x_sorted = [pair[0] for pair in data_pairs]
    y_sorted = [pair[1] for pair in data_pairs]


    x_array = np.array(x_sorted)
    y_array = np.array(y_sorted)

    x_array = x_array / 1000
    y_array = y_array / 1000

    def linear_func (x,a,b):
        return a * x + b


    popt, pcov = optimize.curve_fit(linear_func, x_array, y_array)
    m, n = popt

    m_error = np.sqrt(pcov[0,0])
    n_error = np.sqrt(pcov[1,1])

    y_pred = linear_func(x_array, m, n)
    residuen = y_array - y_pred
    ss_res = np.sum(residuen**2) 
    ss_tot = np.sum((y_array - np.mean(y_array))**2)  
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0


    results = {'m': m, 
               'n': n,
               'm_error': m_error, 
               'n_error': n_error, 
               'r2': r_squared,
               'x_array': x_array,
                'y_array': y_array,
              }
    return results

def extract_water_content(key):
    import re
    match = re.search(r'w(\d+\.?\d*)per|w0per', key)
    if match:
        if match.group(1):
            return match.group(1)
        else:
            return '0'
    if "w0per" in key:
        return '0'
    return None

def extract_pressure(key):
    import re
    match = re.search(r'_(3|6|9|15)kPa$', key)
    if match:
        return f"{match.group(1)}kPa"
    match = re.search(r'(3|6|9|15)kPa', key)
    if match:
        return f"{match.group(1)}kPa"
    return None

def mu_to_phi(mu):
    return np.degrees(np.arctan(mu))

def phi_to_mu(phi):
    return np.tan(np.radians(phi))
        

def linfunc(a,b,x):
    return a * x + b 