def get_parameters():
    config = {}

    config['pattern_size'] = 63
    config['circle_points_number'] = 6
    config['distances'] = _get_distances()

    return config


def _get_distances():
    distances = [3]
    for i in range(20):
        distances.append(distances[i] + i * 2)
    return distances
