# S2S AI competition Datasets

Sub seasonal to Seasonal (S2S) Artificial Intelligence Competition : http://todo.link

In this README is a description of how to get the data for the S2S AI competition. You can find a full description of the dataset here : http://todo.link.int

There are two datasets:
- Reference dataset (only temperature and total precipitation, only 2020, only ECMWF model). Size : >1T.
- Training dataset (not available yet).

There are several ways to use the datasets:
- Direct download (wget, curl, browser). Grib and netCDF format.
- Using climetlab python package. Grib and netCDF and zarr format. Zarr support partial dowload.

# Reference dataset

Data is available weekly every 7 days from 2020-01-02 (every Thurday).

## Direct download 
### GRIB format : 

The list of GRIB files can be found here : 

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/grib/index.html

The URLs are constructed according to the following pattern:

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/grib/{param}-rt-{date}.grib

- {param} is "2t" for surface temperature at 2m, "tp" for total precipitation.
- {date} is the date of retrieval following the YYYYMMDD format.

Example: 

```wget https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/grib/tp-rt-20200102.grib (130M) ```



### NetCDF format

The list of NetCDF files can be found here: 

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/netcdf/index.html

The URLs are constructed according to the following pattern:

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/netcdf/{param}-rt-{date}.nc 

- {param} is "2t" for surface temperature at 2m, "tp" for total precipitation.
- {date} is the date of retrieval following the YYYYMMDD format.

Example:

``` wget https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/netcdf/tp-rt-20200102.nc (130M) ```

## Use the data with climetlab (partial download)

See the [demo notebook](https://nbviewer.jupyter.org/github/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/demo.ipynb) ([src](https://github.com/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/demo.ipynb])). The climetlab python package allows easy access to the data with a few lines of code such as:
```
!pip install climetlab climetlab_s2s_ai_competition
import climetlab as cml
ds = cml.load_dataset("s2s-ai-competition-reference-set", date="20200102", parameter=['2t','tp'])
ds.to_xarray()
```

# Training dataset

TODO
