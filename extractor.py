import math


def describe_point(image, point, pattern, gaussian_kernels_number, parameters):
    gaussian_kernels = _calc_gaussian_kernels(image, point, pattern, gaussian_kernels_number)
    gaussian_kernels_levels = _create_kernel_levels(gaussian_kernels, parameters['circle_points_number'])
    comparisons = _center_comparisons(gaussian_kernels_levels, parameters['levels_to_compare_center'])
    comparisons += _inner_circles_comparisons(gaussian_kernels_levels, parameters['inner_steps'],
                                              parameters['levels_to_compare_inner'])
    comparisons += _circles_comparisons(gaussian_kernels_levels, parameters['outer_steps'], parameters['levels_pairs'])
    return comparisons


def _circles_comparisons(kernel_levels, steps, levels_pairs):
    comparisons = []
    for i in levels_pairs:
        if (i[0] > 0) and (i[0] < len(kernel_levels)) and (i[1] > 0) and (i[1] < len(kernel_levels)):
            comparisons += _circles_all_steps_comparisons(kernel_levels[i[0]], kernel_levels[i[1]], steps)
    return comparisons


def _circles_all_steps_comparisons(kernel1, kernel2, steps):
    comparisons = []
    for i in steps:
        if (i >= 0) and (i < len(kernel1)):
            comparisons.append(_circles_comparison(kernel1, kernel2, i))
    return comparisons


def _circles_comparison(kernel1, kernel2, step):
    level_descriptor = ''
    l = len(kernel1)
    for i in range(l):
        if kernel1[i] > kernel2[(i + step) % l]:
            level_descriptor += '1'
        else:
            level_descriptor += '0'
    return int(level_descriptor, 2)


def _inner_circles_comparisons(kernel_levels, steps, levels_to_compare):
    comparisons = []
    for i in levels_to_compare:
        if (i > 0) and (i < len(kernel_levels)):
            comparisons += _inner_circle_comparisons(kernel_levels[i], steps)
    return comparisons


def _inner_circle_comparisons(kernel_level, steps):
    comparisons = []
    for i in steps:
        if (i > 0) and (i < len(kernel_level)):
            comparisons.append(_inner_circle_comparison(kernel_level, i))
    return comparisons


def _inner_circle_comparison(kernel_level, step):
    level_descriptor = ''
    l = len(kernel_level)
    for i in range(l):
        if kernel_level[i] > kernel_level[(i + step) % l]:
            level_descriptor += '1'
        else:
            level_descriptor += '0'

    return int(level_descriptor, 2)


def _center_comparisons(kernel_levels, levels_to_compare):
    comparisons = []
    for i in levels_to_compare:
        if (i > 0) and (i < len(kernel_levels)):
            comparisons.append(_center_comparison(kernel_levels[i], kernel_levels[0]))
    return comparisons


def _center_comparison(kernel_level, center):
    level_descriptor = ''
    for i in range(len(kernel_level)):
        if center > kernel_level[i]:
            level_descriptor += '1'
        else:
            level_descriptor += '0'
    return int(level_descriptor, 2)


def _create_kernel_levels(kernels, points_number):
    levels_number = int((len(kernels) - 1) / points_number)
    levels = [kernels[0]]
    for i in range(levels_number):
        a = 1 + i * points_number
        b = 1 + (i + 1) * points_number
        levels.append(kernels[a:b])
    return levels


def _calc_gaussian_kernels(image, point, pattern, gaussian_kernels_number):
    kernels = _init_kernels(gaussian_kernels_number)
    half_length = int(math.floor(len(pattern) / 2))
    for i in range(len(pattern)):
        for j in range(len(pattern)):
            for k in pattern[j][i]:
                kernels[k][0] += image[j + point[0] - half_length][i + point[1] - half_length]
                kernels[k][1] += 1
    average_values = []
    for i in range(len(kernels)):
        average_values.append(kernels[i][0] / kernels[i][1])
    return average_values


def _init_kernels(kernels_number):
    kernels = []
    for i in range(kernels_number):
        kernel = [0, 0]
        kernels.append(kernel)
    return kernels
