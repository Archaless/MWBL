# Data QC Prototype
import numpy as np
import pandas as pd

# limits:
tempMax = 50; # C
tempMin = -30 # C
tempWaterMax = 35; # C
tempWaterMin = -3 # C
relHumidMax = 0 # Percent
relHumidMin = 100 # Percent
windSpdMax = 50 # m/s (absolute)
windSpdMin = 0 # m/s (absolute)
windDirMax = 360 # deg.
windDirMin = 0 # deg.

####################################################
                # QC FLAG DEFINITIONS
####################################################

QC_FLAGS = {
    "GOOD": 0,
    "MISSING": 1,
    "RANGE_FAIL": 2,
    "SPIKE": 3,
    "PERSISTENCE": 4,
    "RATE_CHANGE": 5,
    "SPATIAL_FAIL": 6,
    "ML_ANOMALY": 7
}

####################################################
           # 1. MISSING VALUE CHECK
####################################################
def missing_check(series):
    return series.isna()

####################################################
                # 2. RANGE CHECK
####################################################
def range_check(series, min_val, max_val):
    return (series < min_val) | (series > max_val)

####################################################
            # 3. HAMPEL SPIKE FILTER
####################################################
from HampleFilter import hampel_filter

####################################################
        # 4. PERSISTENCE CHECK (STUCK SENSOR)
####################################################
def persistence_check(series, window=10, tolerance=1e-3):
    rolling_std = series.rolling(window).std()
    flags = rolling_std < tolerance

    return flags.fillna(False)

####################################################
            # 5. RATE OF CHANGE CHECK
####################################################
def rate_of_change(series, max_rate):
    diff = series.diff().abs()
    flags = diff > max_rate

    return flags.fillna(False)

####################################################
            # 6. SPATIAL CONSISTENCY CHECK
            # Requires site
####################################################
def spatial_check(df, radius=0.1, threshold=5):
    flags = pd.Series(False, index=df.index)
    for i, row in df.iterrows():
        neighbors = df[
            (abs(df["lat"] - row["lat"]) < radius) &
            (abs(df["lon"] - row["lon"]) < radius) &
            (df.index != i)
        ]
        if len(neighbors) < 2:
            continue
        neighbor_mean = neighbors["value"].mean()
        if abs(row["value"] - neighbor_mean) > threshold:
            flags[i] = True
    
    return flags

####################################################
                # MAIN QC PIPELINE
####################################################
def run_qc_pipeline(
        df,
        min_val=-80,
        max_val=60,
        max_rate=5):
    
    df = df.copy()
    qc_flag = pd.Series(QC_FLAGS["GOOD"], index=df.index)
    missing = missing_check(df["value"])
    qc_flag[missing] = QC_FLAGS["MISSING"]
    range_fail = range_check(df["value"], min_val, max_val)
    qc_flag[range_fail] = QC_FLAGS["RANGE_FAIL"]
    spikes = hampel_filter(df["value"])
    qc_flag[spikes] = QC_FLAGS["SPIKE"]
    persistence = persistence_check(df["value"])
    qc_flag[persistence] = QC_FLAGS["PERSISTENCE"]
    roc = rate_of_change(df["value"], max_rate)
    qc_flag[roc] = QC_FLAGS["RATE_CHANGE"]
    # Spatial check only if 'site' column exists
    if {"site"}.issubset(df.columns):
        spatial = spatial_check(df)
        qc_flag[spatial] = QC_FLAGS["SPATIAL_FAIL"]
    df["qc_flag"] = qc_flag

    return df

####################################################
        # OPTIONAL: REPLACE BAD DATA
####################################################
def replace_bad_data(df):
    df = df.copy()
    df["clean_value"] = df["value"]
    bad = df["qc_flag"] != QC_FLAGS["GOOD"]
    df.loc[bad, "clean_value"] = np.nan
    df["clean_value"] = df["clean_value"].interpolate()

    return df

####################################################
                # EXAMPLE USAGE
####################################################
if __name__ == "__main__":
    df = pd.read_csv("sensor_data.csv", parse_dates=["timestamp"])
    df = df.sort_values("timestamp")
    df = run_qc_pipeline(df)
    #df = replace_bad_data(df)
    print(df.head())

    df.to_csv("qc_output.csv", index=False)