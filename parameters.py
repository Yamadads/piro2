def get_parameters():
    config = {}

    config['pattern_size'] = 63  # window size (odd)
    config['circle_points_number'] = 6  # from 4 to 10
    config['distances'] = _get_distances()  # Rays of successive circles, max distance = 30

    config['levels_to_compare_center'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                          12]  # level IDs to compare with center, can be greater than levels number, from 1 to infinity
    config['inner_steps'] = [1, 2, 3]  # from 1 to half of the circle_points_number
    config['levels_to_compare_inner'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                         12]  # level IDs to compare with center, can be greater than levels number, from 1 to infinity
    return config


def _get_distances():
    distances = [3]
    for i in range(20):
        distances.append(distances[i] + i * 2)
    return distances
