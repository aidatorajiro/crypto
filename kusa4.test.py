from kusa4 import *

test_mat_1 = Mat([1,2,3,4,5,6], 2, 3)
test_mat_2 = Mat([7,8,9,10,11,12], 3, 2)

assert test_mat_1.getrow(0) == [1,2,3]
assert test_mat_1.getrow(1) == [4,5,6]
assert test_mat_1.getcol(1) == [2,5]

assert test_mat_1*test_mat_2 == Mat([58, 64, 139, 154], 2, 2)

test_mat_3 = Mat([1,2,3,4,5,6], 2, 3)
test_mat_3.add_row_vec(1, Vec([1,1,1]))
assert test_mat_3 == Mat([1,2,3,5,6,7], 2, 3)
assert -Vec([1,1,1]) == Vec([-1,-1,-1])
assert -Mat([1,2,3,4,5,6], 2, 3) == Mat([-1,-2,-3,-4,-5,-6], 2, 3)
assert Vec([1,1,1])/2 == Vec([1/2,1/2,1/2])
assert Vec([1,1,1])*2 == Vec([2,2,2])
assert 2/Vec([1,1,1]) == Vec([2,2,2])
assert 2*Vec([1,1,1]) == Vec([2,2,2])

test_mat_4 = Mat([5,3,6,2,6,7,1,3,6], 3, 3)
assert (test_mat_4*dotinv(test_mat_4)).map(lambda x: round(x, 10)) == mat_identity(3)

test_mat_5 = Mat([46, 77, 92, 35, 42, 94, 6, 22, 36, 8, 17, 13, 34, 31, 81, 98, 95, 65, 63, 66, 41, 2, 64, 20, 100, 10, 6, 66, 16, 53, 60, 45, 13, 25, 2, 1, 93, 95, 47, 40, 48, 99, 24, 2, 73, 82, 8, 69, 73, 60, 76, 38, 36, 4, 23, 19, 77, 89, 83, 57, 53, 59, 69, 47, 72, 89, 10, 26, 15, 30, 44, 81, 98, 56, 95, 59, 16, 69, 7, 31, 51, 56, 56, 24, 51, 13, 39, 25, 4, 78, 79, 42, 33, 65, 64, 5, 33, 24, 67, 56], 10, 10)
assert (test_mat_5*dotinv(test_mat_5)).map(lambda x: round(x, 10)) == mat_identity(10)

test_mat_6 = Mat([1,2,3,4,5,6], 2, 3)
assert test_mat_6.map(lambda x: x*x) == test_mat_6.map_dest(lambda x: x*x) == test_mat_6 == Mat([1,4,9,16,25,36], 2, 3)

test_mat_7 = Vec([1,2,3])
assert test_mat_7.map(lambda x: x*x) == test_mat_7.map_dest(lambda x: x*x) == test_mat_7 == Vec([1,4,9])

test_mat_8 = vander(Vec([1,2,3,4,5]), 5)
assert test_mat_8 == Mat([  1,   1,   1,   1,   1,  16,   8,   4,   2,   1,  81,  27,   9,  3,   1, 256,  64,  16,   4,   1, 625, 125,  25,   5,   1], 5, 5)

test_mat_9 = Mat([1,2,3,4,5,5,4,3,2,1,1,2,3,4,5],3,5).t()
assert test_mat_9 == Mat([1,5,1,2,4,2,3,3,3,4,2,4,5,1,5],5,3)

test_mat_10 = Mat(
    [75, 82, 20, 62, 39,
    37, 90, 80, 69, 41,
    39,  4, 39, 42, 12,
    3, 45, 61, 93, 76,
    89, 68, 57, 12, 22,
    70, 26, 61, 89, 80,
    91, 36,  2, 65, 91,
    48, 35, 88, 33, 12,
    78,  5, 84, 20, 50,
    47, 14, 76, 40, 81],10,5)

test_vec_10 = Vec([1,2,3,4,5,6,7,8,9,10])

print(projection(test_mat_10,test_vec_10).map(lambda x: round(x, 10)))

assert projection(test_mat_10,test_vec_10).map(lambda x: round(x, 10)) == Mat([0.03887477, -0.03893069,  0.06069474, -0.03361381,  0.06115582],5,1)

print("all tests passed")