from extractor import describe_point as describe
import sampling_pattern as sp
import copy as copy


class Descriptor(object):
    def __init__(self, parameters):
        self.pattern, self.gaussian_kernels_number = sp.get_sampling_pattern(parameters['pattern_size'],
                                                                             parameters['circle_points_number'],
                                                                             parameters['distances'],
                                                                             parameters['circle_radius_ratio'])
        self.parameters = parameters
        #self.distance_threshold = parameters['distance_threshold']

    def extract(self, image, keypoints):

        descriptions = []
        for image_point in keypoints:
            descriptions.append(
                describe(image, image_point, self.pattern, self.gaussian_kernels_number, self.parameters))
        return descriptions

    def check_similarity(self, descriptor1, descriptor2):
        """
        :param descriptor1: 
        :param descriptor2: 
        :return True if distance between provided descriptors is not greater than threshold, False otherwise: 
        """
        return self.distance(descriptor1, descriptor2, self.parameters) <= self.distance_threshold

    @staticmethod
    def distance(descriptor1, descriptor2, parameters):

        c_descriptor1 = copy.deepcopy(descriptor1)
        c_descriptor2 = copy.deepcopy(descriptor2)

        min_global_distance = len(c_descriptor1) * parameters['circle_points_number']
        shift = 1 << (parameters['circle_points_number'] - 1)
        for i in range(parameters['circle_points_number']):
            distance_sum = 0
            for j in range(len(c_descriptor1)):
                distance_sum += bin(c_descriptor1[j] ^ c_descriptor2[j]).count('1')

            if distance_sum < min_global_distance:
                min_global_distance = distance_sum

            for j in range(len(c_descriptor1)):
                c_descriptor1[j] = Descriptor.left_roll(c_descriptor1[j], parameters['circle_points_number'])

        return min_global_distance / (len(c_descriptor1) * parameters['circle_points_number'])

    @staticmethod
    def left_roll(vector, length):
        return ((vector & 0x1) << (length - 1)) | (vector >> 1)

# int_d1 = int(descriptor1, 2)
# int_d2 = int(descriptor2, 2)
# min_distance = len(descriptor1)
# for i in range(min_distance):
#    specific_distance = bin(int_d1 ^ int_d2).count('1')
#    if specific_distance <= min_distance:
#        min_distance = specific_distance
#    int_d2 = int_d2 >> 1 if int_d2 >= 0 else (int_d2 + 0x100000000) >> 1
# return min_distance


# min_distance = len(descriptor2)
# for i in range(min_distance):
#     descriptor2 = descriptor2[-1] + descriptor2[:-1]
#     specific_distance = sum(d1 != d2 for d1, d2 in zip(descriptor1, descriptor2))
#     if specific_distance <= min_distance:
#         min_distance = specific_distance
# return min_distance
