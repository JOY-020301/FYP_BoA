
import os
from netCDF4 import Dataset
import numpy as np
import glob

def calculate_wind_speed(u, v, scale_factor_u, add_offset_u, scale_factor_v, add_offset_v):
    u = u * scale_factor_u + add_offset_u
    v = v * scale_factor_v + add_offset_v
    return np.sqrt(u**2 + v**2)

def process_file(filepath, output_dir):
    with Dataset(filepath, 'r') as ds:
        # Read dimensions
        longitude = ds.variables['longitude'][:]
        latitude = ds.variables['latitude'][:]
        time = ds.variables['time'][:]

        # Read variables
        u10 = ds.variables['u10'][:]
        v10 = ds.variables['v10'][:]
        u100 = ds.variables['u100'][:]
        v100 = ds.variables['v100'][:]

        # Read scale factors and offsets
        scale_factor_u10 = ds.variables['u10'].scale_factor
        add_offset_u10 = ds.variables['u10'].add_offset
        scale_factor_v10 = ds.variables['v10'].scale_factor
        add_offset_v10 = ds.variables['v10'].add_offset

        scale_factor_u100 = ds.variables['u100'].scale_factor
        add_offset_u100 = ds.variables['u100'].add_offset
        scale_factor_v100 = ds.variables['v100'].scale_factor
        add_offset_v100 = ds.variables['v100'].add_offset

        # Calculate wind speeds
        wind_speed_10m = calculate_wind_speed(u10, v10, scale_factor_u10, add_offset_u10, scale_factor_v10, add_offset_v10)
        wind_speed_100m = calculate_wind_speed(u100, v100, scale_factor_u100, add_offset_u100, scale_factor_v100, add_offset_v100)

        # Create new NetCDF file
        output_filepath = os.path.join(output_dir, os.path.basename(filepath))
        with Dataset(output_filepath, 'w') as new_ds:
            # Copy dimensions
            new_ds.createDimension('longitude', len(longitude))
            new_ds.createDimension('latitude', len(latitude))
            new_ds.createDimension('time', len(time))

            # Create dimension variables
            new_lon = new_ds.createVariable('longitude', 'f4', ('longitude',))
            new_lat = new_ds.createVariable('latitude', 'f4', ('latitude',))
            new_time = new_ds.createVariable('time', 'f4', ('time',))

            new_lon.units = ds.variables['longitude'].units
            new_lat.units = ds.variables['latitude'].units
            new_time.units = ds.variables['time'].units

            new_lon[:] = longitude
            new_lat[:] = latitude
            new_time[:] = time

            # Create new variables for wind speed
            ws10_var = new_ds.createVariable('ws10', 'f4', ('time', 'latitude', 'longitude'))
            ws100_var = new_ds.createVariable('ws100', 'f4', ('time', 'latitude', 'longitude'))

            ws10_var.units = 'm s**-1'
            ws10_var.long_name = '10 metre wind speed'

            ws100_var.units = 'm s**-1'
            ws100_var.long_name = '100 metre wind speed'

            # Assign data to new variables
            ws10_var[:, :, :] = wind_speed_10m
            ws100_var[:, :, :] = wind_speed_100m

            # Copy other variables
            for var_name in ds.variables:
                if var_name not in ['u10', 'v10', 'u100', 'v100', 'longitude', 'latitude', 'time']:
                    var = ds.variables[var_name]
                    new_var = new_ds.createVariable(var_name, var.datatype, var.dimensions)
                    new_var.setncatts({k: var.getncattr(k) for k in var.ncattrs()})
                    new_var[:] = var[:]







def main():  
    # Directory containing the NetCDF files
    input_dir = 'input_path'
    output_dir = 'output_path'
    os.makedirs(output_dir, exist_ok=True)

    # Process each file
    file_paths = glob.glob(os.path.join(input_dir, '*.nc'))
    for file_path in file_paths:
        process_file(file_path, output_dir)
        
        
if __name__ == "__main__":  
    main()