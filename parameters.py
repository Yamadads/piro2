import os as os


class Parameters(object):
    def __init__(self):
        config = {}
        # not set
        config['pattern_size'] = 63  # window size (odd)




        # set

        config['circle_points_number'] = 8  # from 4 to 10
        config['distance_ratio'] = 2  # >0  <5
        config['circle_radius_ratio'] = 0.5  # 0.5 to 0.6 ?

        # auto set

        config['distances'] = self._get_distances(
            config['distance_ratio'])  # Rays of successive circles, max distance = 30
        config['outer_steps'] = [i for i in range(int(
            config['circle_points_number']))]  # [0, 1, 2, 3, 4, 5]  # from 0 to circle_points_number - 1
        # level IDs to compare with center, can be greater than levels number, from 1 to infinity
        config['levels_to_compare_center'] = [i for i in range(1,
            int(len(config['distances']))+1)]  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # from 1 to half of the circle_points_number
        config['inner_steps'] = [i for i in range(int(config['circle_points_number'] / 2))]  # [1, 2, 3]
        # level IDs to compare with center, can be greater than levels number, from 1 to infinity
        config['levels_to_compare_inner'] = [i for i in range(1,
            int(len(config['distances'])+1))]  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        config['levels_pairs'] = self._get_level_pairs(int(len(config['distances'])+1))  # [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8],
        # [8, 9]]  # all pairs to compare from 1 to number of circles


        #config['distance_threshold'] = 0.5

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
    def _get_level_pairs(levels):
        pairs = []
        for i in range(1, levels):
            for j in range(i, levels):
                if j != i:
                    pairs.append([i, j])
        return pairs

    @staticmethod
    def _get_distances(distance_ratio):
        distances = [3]
        for i in range(50):
            distances.append(distances[i] + (i + 1) * distance_ratio)
            if distances[i] > 33:
                break
        return distances
