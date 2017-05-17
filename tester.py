#!/usr/bin/env python
# -*- coding: utf-8 -*-
import descriptor
import sampling_pattern
import cv2
import os.path
import parameters as param


def test_distance_method():
    # for i in range(100000): #100000
    #    test_distance_method()
    descriptor1 = "01110011000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor2 = "01110011000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor3 = "01000011000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor4 = "11100110000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor5 = "11000110000000000000000000000000000000000000000000000000000000000000000000000"
    descriptor6 = "10100110000000000000000010000000000000000000000000000000000000000000000000000"

    check(1, descriptor1, descriptor2, 0)
    check(2, descriptor1, descriptor3, 2)
    check(3, descriptor1, descriptor4, 0)
    check(4, descriptor1, descriptor5, 1)
    check(5, descriptor1, descriptor6, 2)


def check(id, desc1, desc2, correct_value):
    if descriptor.distance(desc1, desc2) != correct_value:
        print("false" + id.__str__())


def check_sampling_pattern():
    params = param.get_parameters()
    sampling_pattern.get_sampling_pattern(params['pattern_size'], params['circle_points_number'], params['distances'])


def load_pictures(directory_path, pictures_no):
    pictures = []
    for i in range(pictures_no):
        str(1).zfill(2)
        img_path = os.path.join(directory_path, str(i).zfill(5) + ".png")
        image = cv2.imread(img_path, 0)
        pictures.append(image)
    return pictures


def calc_descriptors(pictures, pictures_no):
    descriptors = []
    keypoints = [[31, 31]]
    parameters = param.get_parameters()
    for i in range(pictures_no):
        descriptors.append(descriptor.extract(pictures[i], keypoints, parameters))
    return descriptors


def read_maches_file(path):
    matches = []
    with open(path) as f:
        lines = f.read().splitlines()
    print(lines)


def check_descriptor():
    data_path = 'samples/bikes/'
    matches_filename = 'matches.csv'
    pictures_no = 749
    pictures = load_pictures(data_path, pictures_no)
    matches = read_maches_file(data_path + matches_filename)
    calc_descriptors(pictures, pictures_no)


def main():
    check_descriptor()
    # check_sampling_pattern()


if __name__ == '__main__':
    main()
