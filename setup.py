#!/usr/bin/env python
# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


import io
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


package_name = "climetlab-s2s-ai-competition"

version = None
init_py = os.path.join(package_name.replace("-", "_"), "__init__.py")
for line in read(init_py).split("\n"):
    if line.startswith("__version__"):
        version = line.split("=")[-1].strip()[1:-1]
assert version


install_requires = ["requests", "climetlab==0.3.16"]
extras_require = {"zarr": ["zarr", "s3fs"]}

setuptools.setup(
    name=package_name,
    version=version,
    description="Climetlab external dataset plugin for the S2S AI competition organised by ECMWF",
    long_description=read("README.md"),
    author="European Centre for Medium-Range Weather Forecasts (ECMWF)",
    author_email="software.support@ecmwf.int",
    license="Apache License Version 2.0",
    url="https://github.com/ecmwf-lab/climetlab-s2s-ai-competition",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    zip_safe=True,
    entry_points={
        "climetlab.datasets": [
            #            "s2s-ai-competition-validation-set = climetlab_s2s_ai_competition.validation_set",
            # "s2s-ai-competition-reference-set = climetlab_s2s_ai_competition.reference_set",
            #            "s2s-ai-competition-training-set = climetlab_s2s_ai_competition.training_set",
            "s2s-ai-competition-training-set-ecmwf = climetlab_s2s_ai_competition.training_set_ecmwf",
            "s2s-ai-competition-training-set-cwao = climetlab_s2s_ai_competition.training_set_cwao",
            "s2s-ai-competition-training-set-kwbc = climetlab_s2s_ai_competition.training_set_kwbc",
        ]
    },
    keywords="meteorology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
