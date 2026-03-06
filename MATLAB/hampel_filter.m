function outliers = hampel_Filter(data, window_size, n_sigma)
  arguments
    data
    window_size = 5
    n_sigma = 3
  end
  % Vectorized Hampel filter for spike detection
  %
  % Parameters
  % ----------
  % series : numeric vector
  %     Time series data
  % window_size : integer
  %     Half window size
  % n_sigma : integer
  %     Threshold multiplier
  %
  % Returns
  % -------
  % outliers : logical vector
  %     True where outliers are detected
  
  window = 2 * window_size + 1;
  % rolling median
  rolling_median = movmedian(data, window, 'omitnan');
  % absolute deviation from median
  diff_val = abs(data - rolling_median);
  % rolling MAD
  mad = movmedian(diff_val, window, 'omitnan');
  plot(rolling_median)
  hold on
  plot(mad)
  plot(data)
  % scale factor for normal distribution
  threshold = n_sigma * 1.4826 .* mad;
  % outlier detection
  outliers = diff_val > threshold;
  % replace NaNs with false
  outliers(isnan(outliers)) = false;

end

close all
clear
data = sin(-2*pi:0.1:2*pi);
data(7) = 10;
hampel_Filter(data)