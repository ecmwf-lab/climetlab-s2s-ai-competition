# (C) Copyright 2020 ECMWF.  #
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import math
import xarray as xr
import numpy as np

import climetlab as cml
from climetlab import Dataset
from . import S2sDataset


class S2sTrainingSetEcmwf(S2sDataset):
    dataset = "training-set-ecmwf"
    VERSION = "0.1.35"
    origin = "ecmwf"


dataset = S2sTrainingSetEcmwf
