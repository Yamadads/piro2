from extractor import describe_point as describe
import sampling_pattern as sp
import numpy as np


def extract(image, keypoints, parameters):
    pattern, gaussian_kernels_number = sp.get_sampling_pattern(parameters['pattern_size'],
                                                               parameters['circle_points_number'],
                                                               parameters['distances'])
    descriptions = []
    for i in keypoints:
        descriptions.append(describe(image, i, pattern, gaussian_kernels_number, parameters))
    return descriptions


def distance(descriptor1, descriptor2, parameters):
    min_global_distance = len(descriptor1) * parameters['circle_points_number']
    for i in range(parameters['circle_points_number']):
        distance_sum = 0
        for j in range(len(descriptor1)):
            distance_sum += bin(descriptor1[j] ^ descriptor2[j]).count('1')
            descriptor1[j] = descriptor1[j] >> 1 if descriptor1[j] >= 0 else (descriptor1[j] + 0x100000000) >> 1
            descriptor2[j] = descriptor2[j] >> 1 if descriptor2[j] >= 0 else (descriptor2[j] + 0x100000000) >> 1
        if distance_sum < min_global_distance:
            min_global_distance = distance_sum
    return min_global_distance / (len(descriptor1) * parameters['circle_points_number'])

# int_d1 = int(descriptor1, 2)
# int_d2 = int(descriptor2, 2)
# min_distance = len(descriptor1)
# for i in range(min_distance):
#    specific_distance = bin(int_d1 ^ int_d2).count('1')
#    if specific_distance <= min_distance:
#        min_distance = specific_distance
#    int_d2 = int_d2 >> 1 if int_d2 >= 0 else (int_d2 + 0x100000000) >> 1
# return min_distance


# min_distance = len(descriptor2)
# for i in range(min_distance):
#     descriptor2 = descriptor2[-1] + descriptor2[:-1]
#     specific_distance = sum(d1 != d2 for d1, d2 in zip(descriptor1, descriptor2))
#     if specific_distance <= min_distance:
#         min_distance = specific_distance
# return min_distance
