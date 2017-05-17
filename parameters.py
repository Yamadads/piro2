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
    config['outer_steps'] = [0, 1, 2, 3, 4, 5]  # from 0 to circle_points_number - 1
    config['levels_pairs'] = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
                              (8, 9)]  # all pairs to compare from 1 to number of circles
    return config


def _get_distances():
    distances = [3]
    for i in range(50):
        distances.append(distances[i] + i * 2)
    return distances
