import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt



def calculate_spatial_correlation(data):
    time_dim, lat_dim, lon_dim = data.shape
    spatial_corr = np.zeros((time_dim, lat_dim, lon_dim))

    for t in range(time_dim):
        for lat in range(lat_dim):
            for lon in range(lon_dim):
                neighbors = []

                if lat > 0:
                    neighbors.append(data[t, lat - 1, lon])
                if lat < lat_dim - 1:
                    neighbors.append(data[t, lat + 1, lon])
                if lon > 0:
                    neighbors.append(data[t, lat, lon - 1])
                if lon < lon_dim - 1:
                    neighbors.append(data[t, lat, lon + 1])

                if neighbors:
                    spatial_corr[t, lat, lon] = np.nanmean(neighbors)

    return spatial_corr

def calculate_temporal_correlation(data):
    time_dim, lat_dim, lon_dim = data.shape
    temporal_corr = np.zeros((time_dim, lat_dim, lon_dim))

    for t in range(1, time_dim):
        temporal_corr[t, :, :] = data[t - 1, :, :]

    temporal_corr[0, :, :] = np.nan

    return temporal_corr

# Example usage:
# spatial_corr_ws10, temporal_corr_ws10 = calculate_spatial_correlation(normalized_ws10), calculate_temporal_correlation(normalized_ws10)
# spatial_corr_tp, temporal_corr_tp = calculate_spatial_correlation(normalized_tp), calculate_temporal_correlation(normalized_tp)

def process_data_in_chunks(X_train, Y_train, X_test, chunk_size=1000):
    num_test_chunks = len(X_test) // chunk_size + (1 if len(X_test) % chunk_size != 0 else 0)

    all_pred_means = []
    all_pred_vars = []

    kernel = RBF()

    for i in range(num_test_chunks):
        test_start_idx = i * chunk_size
        test_end_idx = min((i + 1) * chunk_size, len(X_test))
        X_test_chunk = X_test[test_start_idx:test_end_idx]

        gp = GaussianProcessRegressor(kernel=kernel)

        # Fit the model on the entire training set and predict the current test chunk
        gp.fit(X_train, Y_train)
        pred_mean, pred_var = gp.predict(X_test_chunk, return_std=True)
        all_pred_means.append(pred_mean)
        all_pred_vars.append(pred_var)

    combined_pred_mean = np.concatenate(all_pred_means)
    combined_pred_var = np.concatenate(all_pred_vars)

    # Ensure the predictions are aligned with the test set size
    return combined_pred_mean[:len(X_test)], combined_pred_var[:len(X_test)]

# Example usage:

# # Process data without correlations
# pred_mean_no_corr, pred_var_no_corr = process_data_in_chunks(X_no_corr_valid, Y_no_corr_valid, X_no_corr_valid)

# # Process data with correlations
# pred_mean_with_corr, pred_var_with_corr = process_data_in_chunks(X_with_corr_valid, Y_with_corr_valid, X_with_corr_valid)