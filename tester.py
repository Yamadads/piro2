#!/usr/bin/env python
# -*- coding: utf-8 -*-
import descriptor as ds
import sampling_pattern
import cv2
import os.path
import os
import parameters as param
import copy


def test_distance_method():

    descriptor1 = "01110011000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor2 = "01110011000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor3 = "01000011000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor4 = "11100110000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor5 = "11000110000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor6 = "10100110000000000000000010000000000000000000000000000000000000000000000000000"

    config = param.Parameters()
    parameters = config.get_parameters()
    descriptor = ds.Descriptor(parameters)

    check(1, descriptor1, descriptor2, 0, parameters, descriptor)
    check(2, descriptor1, descriptor3, 2, parameters, descriptor)
    check(3, descriptor1, descriptor4, 0, parameters, descriptor)
    check(4, descriptor1, descriptor5, 1, parameters, descriptor)
    check(5, descriptor1, descriptor6, 2, parameters, descriptor)


def check(suit_id, desc1, desc2, correct_value, parameters, descriptor):
    if descriptor.distance(desc1, desc2, parameters) != correct_value:
        print("false" + suit_id.__str__())


def check_sampling_pattern():
    params = param.get_parameters()
    sampling_pattern.get_sampling_pattern(params['pattern_size'], params['circle_points_number'], params['distances'])


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


def read_maches_file(path):
    matches = []
    with open(path) as f:
        lines = f.read().splitlines()

    for i in lines:
        line = i.split(",")
        matches.append([int(line[0]), int(line[1])])

    return sorted(matches, key=lambda x: (x[0], x[1]))


def create_bad_matches():
    matches = []
    for i in range(400):
        matches.append([i, 700 - i])
    return matches


def get_matches_results(matches, descriptors, parameters, descriptor):
    for i in range(len(matches)):

        obj_1 = descriptors[matches[i][0]]
        obj_2 = descriptors[matches[i][1]]

        descriptor1 = copy.deepcopy(obj_1[0])
        descriptor2 = copy.deepcopy(obj_2[0])
        matches[i].append(descriptor.distance(descriptor1, descriptor2, parameters))
    return matches


def check_descriptor():

    suite_name = 'bikes'
    data_path = os.path.join('samples', suite_name)
    results_path = os.path.join('results', suite_name)

    matches_filename = 'matches.csv'
    pictures_no = get_pictures_count(data_path)
    pictures = load_pictures(data_path, pictures_no)
    matches = read_maches_file(os.path.join(data_path, matches_filename))

    config = param.Parameters()
    config.dump_to_file(os.path.join(results_path, 'params'))

    parameters = config.get_parameters()

    descriptor = ds.Descriptor(parameters)

    descriptors = calc_descriptors(pictures, pictures_no, descriptor)

    good_matches = get_matches_results(matches, descriptors, parameters, descriptor)
    bad_matches = get_matches_results(create_bad_matches(), descriptors, parameters, descriptor)

    if False:
        print("el1,el2,dist")
        for i in good_matches:
            print(','.join([str(e) for e in i]))

    if True:
        print("el1,el2,dist")
        for i in bad_matches:
            print(','.join([str(e) for e in i]))


def main():
    check_descriptor()
    # check_sampling_pattern()


if __name__ == '__main__':
    # test_distance_method()
    main()
