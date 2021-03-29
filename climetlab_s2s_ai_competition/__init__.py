# (C) Copyright 2020 ECMWF.  #
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


# note : this version number is the plugin version. It has nothing to do with the version number of the dataset
__version__ = "0.4.5"

import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import parameters


URL = "https://storage.ecmwf.europeanweather.cloud"
DATA = "s2s-ai-competition/data"

PATTERN_GRIB = (
    "{url}/{data}/{dataset}-{fctype}-{origin}/{version}/grib/{parameter}-{date}.grib"
)
PATTERN_NCDF = (
    "{url}/{data}/{dataset}-{fctype}-{origin}/{version}/netcdf/{parameter}-{date}.nc"
)
PATTERN_ZARR = (
    # "{url}/{data}/{dataset}-{fctype}-{origin}/{version}/zarr/{parameter}.zarr"
    "{url}/{data}/zarr/{parameter}.zarr"
)

GLOB_ORIGIN = {
    "ecmwf": "ecmf",
    "ecmf": "ecmf",
    "cwao": "cwao",
    "eccc": "cwao",
    "kwbc": "kwbc",
    "ncep": "kwbc",
}

GLOB_FCTYPE = {
    "hindcast": "hindcast",
    "forecast": "forecast",
    "realtime": "forecast",
    "hc": "hindcast",
    "rt": "forecast",
    "fc": "forecast",
}


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

    def __init__(self, origin, version, dataset, fctype):
        self.origin = GLOB_ORIGIN[origin.lower()]
        self.fctype = GLOB_FCTYPE[fctype.lower()]
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
            fctype=self.fctype,
            date=date,
        )
        return request

    def post_xarray_open_dataset_hook(self, ds):
        return ensure_naming_conventions(ds)


def ensure_naming_conventions(ds):
    # we may want also to add this too :
    # import cf2cdm # this is from the package cfgrib
    # ds = cf2cdm.translate_coords(ds, cf2cdm.CDS)
    # or
    # ds = cf2cdm.translate_coords(ds, cf2cdm.ECMWF)

    if "number" in list(ds.coords):
        ds = ds.rename({"number": "realization"})

    if "forecast_time" not in list(ds.coords) and "time" in list(ds.coords):
        ds = ds.rename({"time": "forecast_time"})

    if "step" in list(ds.coords) and "lead_time" not in list(ds.coords):
        ds = ds.rename({"step": "lead_time"})

    if "isobaricInhPa" in list(ds.coords):
        ds = ds.rename({"isobaricInhPa": "plev"})

    # if "plev" in list(ds.coords) and len(ds.coords['plev']) <= 1:
    #    ds = ds.squeeze("plev")
    #    ds = ds.drop("plev")

    if "surface" in list(ds.coords):
        ds = ds.squeeze("surface")
        ds = ds.drop_vars("surface")

    if "heightAboveGround" in list(ds.coords):
        ds = ds.rename({"heightAboveGround": "height_above_ground"})

    if (
        "height_above_ground" in list(ds.coords)
        and len(ds.coords["height_above_ground"]) <= 1
    ):
        ds = ds.squeeze("height_above_ground")
        ds = ds.drop("height_above_ground")

    return ds


class S2sDatasetGRIB(S2sDataset):
    def __init__(self, origin, version, dataset, fctype, *args, **kwargs):
        super().__init__(origin, version, dataset, fctype)
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
    def __init__(self, origin, version, dataset, fctype, *args, **kwargs):
        super().__init__(origin, version, dataset, fctype)
        request = self._make_request(*args, **kwargs)
        self.source = cml.load_source("url-pattern", PATTERN_NCDF, request)


class S2sDatasetZARR(S2sDataset):
    def __init__(self, origin, version, dataset, fctype, *args, **kwargs):
        super().__init__(origin, version, dataset, fctype)

        from climetlab.utils.patterns import Pattern

        request = self._make_request(*args, **kwargs)
        request.pop("date")
        # TODO : remove these pop. leave only the date.
        for k in ["dataset", "origin", "version", "fctype"]:
            request.pop(k)
        urls = Pattern(PATTERN_ZARR).substitute(request)

        self.source = cml.load_source("zarr-s3", urls)


CLASSES = {"grib": S2sDatasetGRIB, "netcdf": S2sDatasetNETCDF, "zarr": S2sDatasetZARR}


class Info:
    def _get_alldates(self, origin, realtime):
        origin = GLOB_ORIGIN[origin]
        # Not used (yet?) by climetlab
        # TODO factorize this code to use it in dataset building
        import pandas as pd

        if origin == "ecmf":
            return pd.date_range(start="2020-01-02", end="2020-12-31", freq="w-thu")
        raise NotImplementedError()


def dataset(dataset, *args, **kwargs):
    return CLASSES[format](*args, **kwargs)
