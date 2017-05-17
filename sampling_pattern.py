import math
import cv2
import numpy as np
from PIL import Image
import copy


def get_sampling_pattern(pattern_size, circle_points_number, distances):
    point_serial_num = int(0)

    sampling_pattern = _init_pattern(pattern_size)
    center_point = _get_pattern_center(pattern_size)
    _set_blurring_points(sampling_pattern, 2, center_point, point_serial_num, pattern_size)
    max_num = _fulfill_pattern(sampling_pattern, center_point, distances, pattern_size, circle_points_number, point_serial_num)
    #image = _create_image(sampling_pattern)
    #show_image('sd', image, 0)
    return sampling_pattern, max_num


def _create_image(pattern):
    image = np.zeros((len(pattern), len(pattern)), np.uint8)
    for i in range(len(pattern)):
        for j in range(len(pattern)):
            if pattern[i][j]:
                if (pattern[i][j][0] > 30) and (pattern[i][j][0] < 1000):
                    image[i][j] = 255
    return image


def _print_pattern(pattern):
    for i in pattern:
        print(i)


def _init_pattern(pattern_size):
    pattern = []
    for i in range(pattern_size):
        pattern_line = []
        for j in range(pattern_size):
            points = []
            pattern_line.append(points)
        pattern.append(pattern_line)
    return pattern


def _get_pattern_center(pattern_size):
    coord = int(math.floor(pattern_size / 2))
    pattern_center = (coord, coord)
    return pattern_center


def _set_blurring_points(pattern, radius, point, point_number, pattern_size):
    for i in range(max(point[0] - int(radius+2), 0), min(point[0] + int(radius + 4), pattern_size - 1)):
        for j in range(max(point[1] - int(radius+2), 0), min(point[1] + int(radius + 4), pattern_size - 1)):
            if _distance_between_points((i, j), point) <= radius + 0.3:  # heheszki wartość z palca
                (pattern[j][i]).append(point_number)


def _set_circle_points(pattern, radius, center, pattern_size, circle_points_number, point_serial_num, start_angle):
    if radius > ((pattern_size / 2) - 3):
        return True, point_serial_num
    point1 = (radius * math.cos(0) + center[0], radius * math.sin(0) + center[1])
    point2 = (radius * math.cos(2 * math.pi / circle_points_number) + center[0],
              radius * math.sin(2 * math.pi / circle_points_number) + center[1])
    circle_radius = _distance_between_points(point1, point2) / 2
    for i in range(circle_points_number):
        point_serial_num += 1
        angle_radians = start_angle + (2 * math.pi / circle_points_number) * i
        x = int(radius * math.cos(angle_radians) + center[1])
        y = int(radius * math.sin(angle_radians) + center[0])
        _set_blurring_points(pattern, circle_radius, (y, x), point_serial_num, pattern_size)
    return False, point_serial_num


def _distance_between_points(point1, point2):
    return math.sqrt(math.pow(point1[1] - point2[1], 2) + math.pow(point1[0] - point2[0], 2))


def _fulfill_pattern(pattern, center, distances, pattern_size, circle_points_number, point_serial_num):
    pattern_full = False
    temp_distances = copy.deepcopy(distances)
    counter = 0
    start_angle = (2 * math.pi / circle_points_number) / 2
    while (not pattern_full) and temp_distances:
        counter += 1
        if counter% 2 == 0:
            angle = start_angle
        else:
            angle = 0
        pattern_full, point_serial_num = _set_circle_points(pattern,
                                                            temp_distances.pop(0),
                                                            center,
                                                            pattern_size,
                                                            circle_points_number,
                                                            point_serial_num,
                                                            angle)
    point_serial_num += 1
    return point_serial_num


def show_image(text, image, time):
    img = Image.fromarray(image)
    img.show()
    img.save('temp.jpg')
