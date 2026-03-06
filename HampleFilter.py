import numpy as np
import pandas as pd

def hampel_filter(series, window_size=5, n_sigma=3):
    """
    Vectorized Hampel filter for spike detection.

    Parameters
    ----------
    series : pandas.Series
        Time series data
    window_size : int
        Half window size
    n_sigma : int
        Threshold multiplier

    Returns
    -------
    pandas.Series (bool)
        True where outliers are detected
    """

    # rolling median
    rolling_median = series.rolling(
        window=2 * window_size + 1,
        center=True
    ).median()

    # absolute deviation from median
    diff = np.abs(series - rolling_median)

    # rolling MAD
    mad = diff.rolling(
        window=2 * window_size + 1,
        center=True
    ).median()

    # scale factor for normal distribution
    threshold = n_sigma * 1.4826 * mad

    outliers = diff > threshold

    return outliers.fillna(False)