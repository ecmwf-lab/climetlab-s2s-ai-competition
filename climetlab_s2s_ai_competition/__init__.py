# (C) Copyright 2020 ECMWF.  #
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


# note this version number has nothing to do with the version number of the dataset
__version__ = "0.3.5"

import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import parameters


URL = "https://storage.ecmwf.europeanweather.cloud"
DATA = "s2s-ai-competition/data"
PATTERN = "{url}/{data}/{dataset}/{version}/{format}/{fctype}/{origin}/{parameter}-{date}.{extension}"
ZARRPATTERN = "{url}/{data}/{format}/{parameter}.{extension}"
# this is the default version of the dataset


class S2sDataset(Dataset):
    name = None
    home_page = "-"
    licence = "https://apps.ecmwf.int/datasets/data/s2s/licence/"
    # TODO : upload a json file next to the dataset and read it
    documentation = "-"
    citation = "-"
    VERSION = "0.1.36"  # will be modified by the datasets

    terms_of_use = (
        "By downloading data from this dataset, you agree to the their terms: "
        "Attribution 4.0 International(CC BY 4.0). If you do not agree with such terms, "
        "do not download the data. For more information, please visit https://www.ecmwf.int/en/terms-use "
        "and https://apps.ecmwf.int/datasets/data/s2s/licence/."
    )

    dataset = None

    def __init__(self):
        pass

    def _load(self, *args, **kwargs):
        format = kwargs.pop("format", "grib")
        load = getattr(self, f"_load_{format}")
        return load(*args, **kwargs)

    # latter on, we want also to support stacking decorators
    #    @parameters(parameter=("parameter-list", "mars"))
    #    @parameters(date=("date-list", "%Y%m%d"))
    @parameters(parameter=("parameter-list", "mars"), date=("date-list", "%Y%m%d"))
    def _make_request(
        self,
        date=None,
        parameter="tp",
        hindcast=False,
        version=None,
    ):
        if version is None:
            version = self.VERSION
        request = dict(
            url=URL,
            data=DATA,
            dataset=self.dataset.replace("training", "train"),  # todo fix the data link
            origin=self.origin,
            version=version,
            parameter=parameter,
            fctype="hc" if hindcast else "rt",
            date=date,
        )
        return request

    def _load_grib(self, *args, **kwargs):
        request = self._make_request(*args, **kwargs)
        request["format"] = "grib"
        request["extension"] = "grib"
        self.source = cml.load_source("url-pattern", PATTERN, request)

    #        for s in self.source.sources:
    #            print(s)
    #            print(s.dataset)
    #            s.dataset = self

    def _load_netcdf(self, *args, **kwargs):
        request = self._make_request(*args, **kwargs)
        request["format"] = "netcdf"
        request["extension"] = "nc"
        self.source = cml.load_source("url-pattern", PATTERN, request)

    def _load_zarr(self, *args, **kwargs):

        from climetlab.utils.patterns import Pattern

        request = self._make_request(*args, **kwargs)
        request["format"] = "zarr"
        request["extension"] = "zarr"
        request.pop("fctype")
        request.pop("date")
        request.pop("dataset")
        request.pop("version")

        urls = Pattern(ZARRPATTERN).substitute(request)

        self.source = cml.load_source("zarr-s3", urls)

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

    def cfgrib_options(self, time_convention="withstep"):
        params = {}
        if time_convention == "withstep":
            time_dims = ["time", "step"]  # this is the default of engine='cfgrib'
            chunk_sizes_in = {
                "time": 1,
                "latitude": None,
                "longitude": None,
                "number": 1,
                "step": 1,
            }

        elif time_convention == "nostep":
            time_dims = ["time", "valid_time"]
            chunk_sizes_in = {
                "time": 1,
                "latitude": None,
                "longitude": None,
                "number": 1,
                "valid_time": 1,
            }

        else:
            raise Exception()

        # params['engine'] = 'cfgrib'
        params["chunks"] = chunk_sizes_in
        params["backend_kwargs"] = dict(squeeze=False, time_dims=time_dims)

        return params
