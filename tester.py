#!/usr/bin/env python
# -*- coding: utf-8 -*-
import descriptor as ds
import cv2
import os.path
import os
import parameters as param
import random as rand
import numpy as np
import multiprocessing as mp
import joblib as jb


def get_pictures_count(directory_path):

    return len([name for name in os.listdir(directory_path) if name.endswith(".png")])


def load_pictures(directory_path, pictures_no):
    pictures = []

    for i in range(pictures_no):
        str(1).zfill(2)
        img_path = os.path.join(directory_path, str(i).zfill(5) + ".png")
        image = cv2.imread(img_path, 0)
        pictures.append(image)
    return pictures


def calc_descriptors(pictures, pictures_no, descriptor):
    descriptors = []
    keypoints = [[31, 31]]
    for i in range(pictures_no):
        descriptors.append(descriptor.extract(pictures[i], keypoints))
    return descriptors


def read_matches_file(path):
    matches = []
    with open(path) as f:
        lines = f.read().splitlines()

    for i in lines:
        line = i.split(",")
        matches.append([int(line[0]), int(line[1])])

    return sorted(matches, key=lambda x: (x[0], x[1]))


def create_bad_matches(pictures_no, matches):

    reserved = {}

    rand.seed()

    for pair in matches:
        if pair[0] < pair[1]:
            reserved['.'.join(map(str, pair))] = True
        else:
            reserved['.'.join(map(str, [pair[1], pair[0]]))] = True

    bad_matches = []

    while len(bad_matches) < pictures_no:

        num_1 = rand.randint(0, pictures_no - 2)
        num_2 = rand.randint(num_1 + 1, pictures_no - 1)

        s_id = '.'.join(map(str, [num_1, num_2]))

        if s_id not in reserved:
            reserved[s_id] = True
            bad_matches.append([num_1, num_2])

    return bad_matches


def get_matches_results(matches, descriptors, parameters, descriptor):
    for i in range(len(matches)):
        matches[i].append(descriptor.distance(descriptors[matches[i][0]][0], descriptors[matches[i][1]][0], parameters))
    return matches


def get_results_mean(matches, descriptors, parameters, descriptor):

    result = []

    for i in range(len(matches)):
        result.append(descriptor.distance(descriptors[matches[i][0]][0], descriptors[matches[i][1]][0], parameters))

    return np.mean(result)


def create_configurations():

    configurations = []

    for circle_points_number in range(4, 11):
        for inner_steps in range(1, int(circle_points_number / 2)):
            for levels_to_compare_center in [i for i in [1, 3, 7] if i <= circle_points_number]:
                for levels_to_compare_inner in [i for i in [1, 3, 7] if i <= circle_points_number]:
                    for outer_steps in [i for i in [1, 3, 7] if i <= circle_points_number]:
                        configurations.append([
                            circle_points_number, inner_steps, levels_to_compare_center, levels_to_compare_inner, outer_steps
                        ])

    return configurations


def calculate_mean(results_path, pictures, pictures_no, matches, bad_matches, configuration):
    config = param.Parameters()

    circle_points_number = configuration[0]
    inner_steps = configuration[1]
    levels_to_compare_center = configuration[2]
    levels_to_compare_inner = configuration[3]
    outer_steps = configuration[4]

    config.set('circle_points_number', circle_points_number)

    config.set('inner_steps', [i for i in range(1, int(circle_points_number / 2))])
    config.set('levels_to_compare_center', [i for i in [1, 3, 7] if i <= levels_to_compare_center])
    config.set('levels_to_compare_inner', [i for i in [1, 3, 7] if i <= levels_to_compare_inner])
    config.set('outer_steps', [i for i in [1, 3, 7] if i <= outer_steps])

    parameters = config.get_parameters()

    suite_name = 'params_{0}_{1}_{2}_{3}_{4}'.format(
        circle_points_number, inner_steps, levels_to_compare_center, levels_to_compare_inner, outer_steps
    )

    dump_file_name = os.path.join(results_path, suite_name)

    descriptor = ds.Descriptor(parameters)

    descriptors = calc_descriptors(pictures, pictures_no, descriptor)

    good_matches_mean = get_results_mean(matches, descriptors, parameters, descriptor)
    bad_matches_mean = get_results_mean(bad_matches, descriptors, parameters, descriptor)

    mean_difference = bad_matches_mean - good_matches_mean

    with open(dump_file_name, "w+") as dump:
        dump.write('# Results section (good_mean, bad_mean, mean_difference\n')
        dump.write(','.join(map(str, [good_matches_mean, bad_matches_mean, mean_difference, '\n'])))

    config.dump_to_file(dump_file_name)

    result = ','.join(map(str, [suite_name, good_matches_mean, bad_matches_mean, mean_difference]))
    # print("good matches mean is {0}".format(good_matches_mean))
    # print("bad matches mean is {0}".format(bad_matches_mean))

    return result


def check_descriptor():

    suite_name = 'leuven'
    data_path = os.path.join('samples', suite_name)
    results_path = os.path.join('results', suite_name)

    matches_filename = 'matches.csv'
    pictures_no = get_pictures_count(data_path)
    pictures = load_pictures(data_path, pictures_no)

    matches = read_matches_file(os.path.join(data_path, matches_filename))
    bad_matches = create_bad_matches(pictures_no, matches)

    print("Data initialized")

    num_cores = mp.cpu_count()
    print('cpu count {0}'.format(num_cores))

    configurations = create_configurations()

    results = jb.Parallel(n_jobs=num_cores)(jb.delayed(calculate_mean)(
        results_path, pictures, pictures_no, matches, bad_matches, configurations[i]
    ) for i in range(10))

    with open(os.path.join(results_path, 'master_results'), "w+") as dump:
        dump.write('suite_name, good_match_dist, bad_match_dist, diff\n')
        for line in results:
            dump.write(''.join([line, '\n']))

    print('tests end')

    # good_matches = get_matches_results(matches, descriptors, parameters, descriptor)
    # bad_matches = get_matches_results(bad_matches, descriptors, parameters, descriptor)
    #
    # if False:
    #     print("el1,el2,dist")
    #     for i in good_matches:
    #         print(','.join([str(e) for e in i]))
    #
    # if True:
    #     print("el1,el2,dist")
    #     for i in bad_matches:
    #         print(','.join([str(e) for e in i]))


def main():
    check_descriptor()


if __name__ == '__main__':
    # test_distance_method()
    main()
