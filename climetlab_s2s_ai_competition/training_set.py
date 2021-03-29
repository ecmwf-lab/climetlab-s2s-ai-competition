from . import CLASSES


def dataset(
    format="grib", origin="ecmwf", fctype="forecast", version="0.1.42", *args, **kwargs
):
    return CLASSES[format](
        origin=origin,
        version=version,
        dataset="training-set",
        fctype=fctype,
        *args,
        **kwargs
    )
