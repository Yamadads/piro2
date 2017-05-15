import math


def describe_point(image, point, pattern_size):
    sub_image = _get_subimage(image, point, pattern_size)
    return 0


def _get_subimage(image, point, pattern_size):
    size = math.foor(pattern_size / 2)
    sub_image = image[point[0] - size: point[0] + size][point[1] - size:point[1] + size]
    print(sub_image)
    return sub_image
