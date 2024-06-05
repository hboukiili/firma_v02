import cdsapi
import xarray as xr
import io
import tempfile


c = cdsapi.Client(
    url= "https://cds.climate.copernicus.eu/api/v2",
    key= "313656:98e3f8b6-e2d6-4207-b4c0-0c96d0ca2fd1"
)


buffer = io.BytesIO()

with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as tmp:
            c.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis',
                    'variable': [
                        '2m_temperature',
                    ],
                    'year': '2023',
                    'month': '06',
                    'day': '01',
                    'time': [
                        '11:00',
                    ],
                    'format': 'netcdf',
                },
                tmp.name
            )

print("done getting data for : ", c.cdm.get_coordinates(tmp.name))
ds = xr.open_dataset(tmp.name, engine='netcdf4')

hours_data = ds.sel(time=ds['time.hour'].isin([11]))

data_dict = {
    'time': hours_data['time'].values.tolist(),
    '2m_temperature': hours_data['t2m'].values.tolist(),
    'total_precipitation': hours_data['tp'].values.tolist(),
}

print(data_dict['time'])