import os as os


class Parameters(object):
    def __init__(self):
        config = {}

        config['pattern_size'] = 63  # window size (odd)
        config['circle_points_number'] = 8  # from 4 to 10
        config['distances'] = self._get_distances()  # Rays of successive circles, max distance = 30

        # level IDs to compare with center, can be greater than levels number, from 1 to infinity
        config['levels_to_compare_center'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        # from 1 to half of the circle_points_number
        config['inner_steps'] = [i for i in range(int(config['circle_points_number'] / 2))]  # [1, 2, 3]

        # level IDs to compare with center, can be greater than levels number, from 1 to infinity
        config['levels_to_compare_inner'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        config['outer_steps'] = [0, 1, 2, 3, 4, 5]  # from 0 to circle_points_number - 1

        config['levels_pairs'] = self._get_level_pairs()  # [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8],
        # [8, 9]]  # all pairs to compare from 1 to number of circles

        config['circle_radius_ratio'] = 0.5 #0.5 to 0.6 ?
        config['distance_threshold'] = 0.5

        self.config = config

    def set(self, name, value):
        self.config[name] = value

    def get_parameters(self):
        return self.config

    def dump_to_file(self, filepath):
        with open(filepath, "a") as dump:
            dump.write('# Params section\n')
            for entry in self.config:
                dump.write(','.join([entry, str(self.config[entry]), '\n']))

    @staticmethod
    def _get_level_pairs():
        pairs = []
        for i in range(15):
            for j in range(15):
                pairs.append([i, j])
        return pairs

    @staticmethod
    def _get_distances():
        distances = [3]
        for i in range(50):
            distances.append(distances[i] + i * 2)
        return distances
