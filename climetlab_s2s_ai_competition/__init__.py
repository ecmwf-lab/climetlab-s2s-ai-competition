# (C) Copyright 2020 ECMWF.  #
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


# note this version number has nothing to do with the version number of the dataset
__version__ = "0.3.7"

import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import parameters


URL = "https://storage.ecmwf.europeanweather.cloud"
DATA = "s2s-ai-competition/data"

PATTERN_GRIB = "{url}/{data}/{dataset}/{version}/grib/{parameter}-{date}.grib"
PATTERN_NCDF = "{url}/{data}/{dataset}/{version}/netcdf/{parameter}-{date}.nc"
PATTERN_ZARR = "{url}/{data}/zarr/{parameter}.zarr"

GLOB_ORIGIN = {
    "ecmwf": "ecmf",
    "ecmf": "ecmf",
    "cwao": "cwao",
    "eccc": "cwao",
    "kwbc": "kwbc",
    "ncep": "kwbc",
}

# Hindcast and Forecasts are two different datasets. No more argument to choose betwen them.
# GLOB_FCTYPE = {
#     "hindcast": "hindcast",
#     "forecast": "forecast",
#     "realtime": "forecast",
#     "hc": "hindcast",
#     "rt": "forecast",
#     "fc": "forecast"
# }

class S2sDataset(Dataset):
    name = None
    home_page = "-"
    licence = "https://apps.ecmwf.int/datasets/data/s2s/licence/"
    # TODO : upload a json file next to the dataset and read it
    documentation = "-"
    citation = "-"

    terms_of_use = (
        "By downloading data from this dataset, you agree to the terms and conditions defined at "
        "https://apps.ecmwf.int/datasets/data/s2s/licence/. "
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    def __init__(self, origin, version, dataset):
        origin = GLOB_ORIGIN[origin.lower()]
        self.origin = origin
        self.version = version
        self.dataset = dataset

    # latter on, we want also to support stacking decorators
    #    @parameters(parameter=("parameter-list", "mars"))
    #    @parameters(date=("date-list", "%Y%m%d"))
    @parameters(parameter=("parameter-list", "mars"), date=("date-list", "%Y%m%d"))
    def _make_request(
        self,
        date="20200102",
        parameter="tp",
        hindcast=False,
    ):
        request = dict(
            url=URL,
            data=DATA,
            dataset=self.dataset,
            origin=self.origin,
            version=self.version,
            parameter=parameter,
#            fctype="hc" if hindcast else "rt",
            date=date,
        )
        return request

    def post_xarray_open_dataset_hook(self, ds):
        # we may want also to add this too :
        # import cf2cdm # this is from the package cfgrib
        # ds = cf2cdm.translate_coords(ds, cf2cdm.CDS)
        # or
        # ds = cf2cdm.translate_coords(ds, cf2cdm.ECMWF)

        if "number" in list(ds.coords):
            ds = ds.rename({"number": "realization"})

        if "time" in list(ds.coords):
            ds = ds.rename({"time": "forecast_time"})

        if "valid_time" in list(ds.coords):
            ds = ds.rename({"valid_time": "time"})

        if "heightAboveGround" in list(ds.coords):
            # if we decide to keep it, rename it.
            # ds = ds.rename({'heightAboveGround':'height_above_ground'})
            ds = ds.squeeze("heightAboveGround")
            ds = ds.drop_vars("heightAboveGround")

        if "surface" in list(ds.coords):
            ds = ds.squeeze("surface")
            ds = ds.drop_vars("surface")

        return ds


class S2sDatasetGRIB(S2sDataset):
    def __init__(self, origin, version, dataset, *args, **kwargs):
        super().__init__(origin, version, dataset)
        request = self._make_request(*args, **kwargs)
        self.source = cml.load_source("url-pattern", PATTERN_GRIB, request)

    def cfgrib_options(self, time_convention="withstep"):
        params = {}
        assert time_convention in ("withstep", "nostep")

        if time_convention == "withstep":
            time_dims = ["time", "step"]  # this is the default of engine='cfgrib'
            chunk_sizes_in = {
                "time": 1,
                "latitude": None,
                "longitude": None,
                "number": 1,
                "step": 1,
            }

        if time_convention == "nostep":
            time_dims = ["time", "valid_time"]
            chunk_sizes_in = {
                "time": 1,
                "latitude": None,
                "longitude": None,
                "number": 1,
                "valid_time": 1,
            }

        params["chunks"] = chunk_sizes_in
        params["backend_kwargs"] = dict(squeeze=False, time_dims=time_dims)

        return params


class S2sDatasetNETCDF(S2sDataset):
    def __init__(self, origin, version, dataset, *args, **kwargs):
        super().__init__(origin, version, dataset)
        request = self._make_request(*args, **kwargs)
        self.source = cml.load_source("url-pattern", PATTERN_NCDF, request)


class S2sDatasetZARR(S2sDataset):
    def __init__(self, origin, version, dataset, *args, **kwargs):
        super().__init__(origin, version, dataset)

        from climetlab.utils.patterns import Pattern

        request = self._make_request(*args, **kwargs)
        urls = Pattern(PATTERN_ZARR).substitute(request)

        self.source = cml.load_source("zarr-s3", urls)


CLASSES = {"grib": S2sDatasetGRIB, "netcdf": S2sDatasetNETCDF, "zarr": S2sDatasetZARR}


def dataset(
    format="grib", origin="ecmf", version="0.1.42", dataset="training-set", **kwargs
):
    return CLASSES[format](origin, version, dataset, **kwargs)
