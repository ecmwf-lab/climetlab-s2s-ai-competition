# S2S AI competition Datasets

Sub seasonal to Seasonal (S2S) Artificial Intelligence Competition : http://todo.link

In this README is a description of how to get the data for the S2S AI competition. You can find a full description of the dataset here : http://todo.link.int

There are two datasets:
- Training dataset from three different models : ECMWF, ECCC, NCEP. Each of these three datasets are splitted into two forecast types : fctype='forecast' and fctype='hindcast' data. This gives 6 datasets :
  -  training-set-forecast-ecmf [grib](https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-ecmwf/0.1.43/grib/index.html)   [netcdf](https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-ecmf/0.1.43/netcdf/index.html)
  -  training-set-forecast-cwao [grib](https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-cwao/0.1.43/grib/index.html)   [netcdf](https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-cwao/0.1.43/netcdf/index.html)
  -  training-set-forecast-kwbc [grib](https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-kwbc/0.1.43/grib/index.html)  [netcdf](https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-kwbc/0.1.43/netcdf/index.html)
  -  training-set-hindcast-ecmf (not fully uploaded yet)
  -  training-set-hindcast-cwao (not fully uploaded yet)
  -  training-set-hindcast-kwbc (not fully uploaded yet)
- Benchmark dataset (TBD) (only temperature and total precipitation, only 2020, only ECMWF model). Size : >1T.
- Verification dataset (TBD)

There are several ways to use the datasets:
- Direct download (wget, curl, browser). Grib and netCDF format.
- Using climetlab python package. Grib and netCDF and zarr format. Zarr is a cloud-friendly data format and support partial dowload (experimental).

# Training dataset

Data is available weekly every 7 days from 2020-01-02 (every Thurday).

## Direct download 
### GRIB format : 

The list of GRIB files for the 'training-set-forecast-cwao' dataset can be found at : 

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-cwao/0.1.43/grib/index.html

The URLs are constructed according to the following pattern:

https:<span></span>//storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/{datasetname}/0.1.43/grib/{param}-rt-{date}.grib

- {param} is "2t" for surface temperature at 2m, "tp" for total precipitation.
- {date} is the date of retrieval following the YYYYMMDD format.

Example to retrieve the file with wget :

``` wget https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-cwao/0.1.43/grib/tp-20200102.grib (130M) ```


### NetCDF format

The list of NetCDF files for the 'training-set-forecast-cwao' dataset can be found at : 

https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-cwao/0.1.43/netcdf/index.html

The URLs are constructed according to the following pattern:

https:<span></span>//storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/{datasetname}/0.1.43/netcdf/{param}-rt-{date}.nc

- {param} is "2t" for surface temperature at 2m, "tp" for total precipitation.
- {date} is the date of retrieval following the YYYYMMDD format.

Example to retrieve the file with wget :

``` wget https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-cwao/0.1.43/netcdf/tp-20200102.nc (130M) ```

### Zarr format (experimental).

The zarr storage location include all the reference data. The zarr urls are **not** designed to be open in a browser (see [zarr](https://zarr.readthedocs.io/en/stable)):
https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/training-set-forecast-cwao/0.1.43/zarr/index.html

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
ds = cml.load_dataset("s2s-ai-competition-training-set", origin="cwao", fctype="forecast", date="20200102", parameter='2t')
ds.to_xarray()
```
