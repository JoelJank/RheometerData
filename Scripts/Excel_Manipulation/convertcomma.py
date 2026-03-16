import pandas as pd
import numpy as np
import re

df = pd.read_csv(
    "C:\\AGParteli\\90micron.csv",
    dtype=str,
    quotechar='"',
    sep=None,
    engine='python'
)

def clean_and_convert_to_float(wert):
    if pd.isna(wert) or wert == '':
        return np.nan
    
    wert_str = str(wert).strip()
    wert_str = re.sub(r'[^\d\.,-]', '', wert_str)
    wert_str = wert_str.replace(',', '.')
    
    if wert_str.count('.') > 1:
        teile = wert_str.split('.')
        wert_str = teile[0] + '.' + ''.join(teile[1:])
    
    try:
        return float(wert_str)
    except:
        try:
            return float(re.sub(r'[^\d-]', '', wert_str))
        except:
            return np.nan

for col in df.columns:
    print(f"\n🔄 Verarbeite Spalte: '{col}'")
    
    print(f"  Original (erste 3): {df[col].iloc[:3].tolist()}")
    
    df[col] = df[col].apply(clean_and_convert_to_float)
    
    print(f"  Konvertiert (erste 3): {df[col].iloc[:3].tolist()}")
    
    print(f"  Datentyp: {df[col].dtype}")

df = df.dropna(how='all')

output_file = "C:\\AGParteli\\RheometerData\\Data\\Glass\\90 micron\\bigcup\\w0per_3_6_15_kPa\\w0per_3_6_15_kPa_original.xlsx"
df.to_excel(output_file, index=False)