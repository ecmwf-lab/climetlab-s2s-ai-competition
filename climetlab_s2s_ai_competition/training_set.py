from . import CLASSES


def dataset(format="grib", origin="ecmf", version="0.1.36", *args, **kwargs):
    return CLASSES[format](origin, version, dataset="training-set", *args, **kwargs)
