from brisk import describe_point as brisk_describe


def extract(image, keypoints):
    descriptions = []
    for i in keypoints:
        descriptions.append(brisk_describe(image, keypoints[i]))
    return descriptions


def distance(descriptor1, descriptor2):
    return 0
