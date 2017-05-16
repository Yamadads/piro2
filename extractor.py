import math


def describe_point(image, point, pattern, gaussian_kernels_number, parameters):
    gaussian_kernels = _calc_gaussian_kernels(pattern, gaussian_kernels_number)

    return 0


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
    for i in range(len(kernels_number)):
        kernel = [0, 0]
        kernels.append(kernel)
    return kernels
