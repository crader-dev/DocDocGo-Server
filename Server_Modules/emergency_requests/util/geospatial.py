""" Geospatial utility functions
"""

from math import radians, cos, sin, asin, sqrt


def haversine_distance(lat1, long1, lat2, long2):
    """
    Calculate the distance (in miles) between two lat/long (in decimal degrees) points on Earth.
    Based on: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    # haversine formula
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3956  # In miles
    return c * r

