import cdsapi
import xarray as xr
import os

def download_and_resample(year, variables, area, output_filename):
    # Initialize the API client
    c = cdsapi.Client()

    # Define the two halves of the year
    first_half_months = ['01', '02', '03', '04', '05', '06']
    second_half_months = ['07', '08', '09', '10', '11', '12']
    days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

    def download_and_resample_half(year, months, filename):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Retrieve the data
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': variables,
                'year': str(year),
                'month': months,
                'day': days,
                'time': [
                    '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',
                ],
                'area': area,
            },
            filename
        )

        # Load the data using xarray
        ds = xr.open_dataset(filename)

        # Resample to daily frequency and take the maximum value for each variable
        daily_max = ds.resample(time='1D').max()

        # Save the processed data to a temporary NetCDF file
        temp_filename = f'{os.path.splitext(filename)[0]}_daily_max.nc'
        daily_max.to_netcdf(temp_filename)
        return temp_filename

    # Download and resample the first half of the year
    first_half_filename = download_and_resample_half(year, first_half_months, f'data/{year}_first_half.nc')

    # Download and resample the second half of the year
    second_half_filename = download_and_resample_half(year, second_half_months, f'data/{year}_second_half.nc')

    # Load the two halves
    ds_first_half = xr.open_dataset(first_half_filename)
    ds_second_half = xr.open_dataset(second_half_filename)

    # Combine the two halves
    combined = xr.concat([ds_first_half, ds_second_half], dim='time')

    # Save the combined data to a new NetCDF file
    combined.to_netcdf(output_filename)

    # Clean up temporary files
    os.remove(first_half_filename)
    os.remove(second_half_filename)

# Example usage: Uncomment if you want to run this script
# year = 2008
# variables = [
#     '10m_u_component_of_wind', '10m_v_component_of_wind', '100m_u_component_of_wind', '100m_v_component_of_wind', '10m_wind_gust_since_previous_post_processing',
#     'large_scale_precipitation', 'total_precipitation'
# ]
# area = [22, -95, 32, -70]  # Adjust this based on the specific area of interest
# output_filename = f'data/{year}_daily_max.nc'

# download_and_resample(year, variables, area, output_filename)
# os.remove(f'data/{year}_first_half.nc')
# os.remove(f'data/{year}_second_half.nc')