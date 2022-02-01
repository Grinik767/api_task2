from math import asin, cos, sin, radians, sqrt


def zoom_toponym_one_object(lc, uc):
    size_x = abs(lc[0] - uc[0]) / 2
    size_y = abs(lc[1] - uc[1]) / 2
    return ','.join([str(size_x), str(size_y)])


def zoom_toponym_two_object(lc, uc):
    size_x = abs(lc[0] - uc[0])
    size_y = abs(lc[1] - uc[1])
    return ','.join([str(size_x), str(size_y)])


def get_max_zoom(lc1, uc1, lc2, uc2):
    lc = [min(lc1[0], lc2[0]), min(lc1[1], lc2[1])]
    uc = [max(uc1[0], uc2[0]), max(uc1[1], uc2[1])]
    return lc, uc


def count_distance(lat1, long1, lat2, long2):
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)
    u = sin((lat2 - lat1) / 2)
    v = sin((long2 - long1) / 2)
    l = 2 * 6371 * asin(sqrt(u * u + cos(lat1) * cos(lat2) * v * v))
    return f'{l:.2f}'