# S2S AI competition Datasets

Sub seasonal to Seasonal (S2S) Artificial Intelligence Competition : http://todo.link

In this README is a description of how to get the data for the S2S AI competition. You can find a full description of the dataset here : http://todo.link.int

There are two datasets:
- Reference dataset (only temperature and total precipitation, only 2020, only ECMWF model). Size : >1T.
- Training dataset (not available yet).

There are several ways to use the datasets:
- Direct download (wget, curl, browser). Grib and netCDF format.
- Using climetlab python package. Grib and netCDF and zarr format. Zarr is a cloud-friendly data format and support partial dowload (experimental).

# Reference dataset

Data is available weekly every 7 days from 2020-01-02 (every Thurday).

## Direct download 
### GRIB format : 

The list of GRIB files can be found here : 

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/grib/index.html

The URLs are constructed according to the following pattern:

https:<span></span>//storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/grib/{param}-rt-{date}.grib

- {param} is "2t" for surface temperature at 2m, "tp" for total precipitation.
- {date} is the date of retrieval following the YYYYMMDD format.

Example: 

```wget https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/grib/tp-rt-20200102.grib (130M) ```



### NetCDF format

The list of NetCDF files can be found here: 

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/netcdf/index.html

The URLs are constructed according to the following pattern:

https:<span></span>//storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/netcdf/{param}-rt-{date}.nc 

- {param} is "2t" for surface temperature at 2m, "tp" for total precipitation.
- {date} is the date of retrieval following the YYYYMMDD format.

Example:

``` wget https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/netcdf/tp-rt-20200102.nc (130M) ```

### Zarr format (experimental).

The zarr storage location include all the reference data. The following link is **not** to be open in a browser :
https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/1.0.0/zarr/

While accessing the zarr storage without climetlab may be possible, we recommend using climetlab with this plugin (climetlab-s2s-ai-competition)


## Use the data with climetlab (supports grib, netcdf and zarr)

See the demo notebooks here (https://github.com/ecmwf-lab/climetlab-s2s-ai-competition/notebooks) : 
- Netcdf [nbviewer](https://nbviewer.jupyter.org/github/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/notebooks/demo_netcdf.ipynb) [colab](https://colab.research.google.com/github/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/notebooks/demo_netcdf.ipynb)
- Grib [nbviewer](https://nbviewer.jupyter.org/github/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/notebooks/demo_grib.ipynb) [colab](https://colab.research.google.com/github/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/notebooks/demo_grib.ipynb)
- Zarr [nbviewer](https://nbviewer.jupyter.org/github/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/notebooks/demo_zarr.ipynb) [colab](https://colab.research.google.com/github/ecmwf-lab/climetlab-s2s-ai-competition/blob/master/notebooks/demo_zarr.ipynb)  <span style="color:red;">(experimental)</span> .

The climetlab python package allows easy access to the data with a few lines of code such as:
```
!pip install climetlab climetlab_s2s_ai_competition
import climetlab as cml
ds = cml.load_dataset("s2s-ai-competition-reference-set", date="20200102", parameter=['2t','tp'])
ds.to_xarray()
```

# Training dataset

Not available yet.
