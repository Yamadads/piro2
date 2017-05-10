#!/usr/bin/env python
# -*- coding: utf-8 -*-
import descriptor


def test_distance_method():
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


def main():
    for i in range(100000): #100000
        test_distance_method()


if __name__ == '__main__':
    main()
