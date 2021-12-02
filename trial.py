# x = [1,1,1,2,2,2,3,4]
# # {1:3, 2:3, 3:1, 4:1}
# dict_ = {}
# # count = 0
# for i in x:
#     if i not in dict_:
#         dict_[i] = 1
#     else:
#         dict_[i] += 1
# new = tuple(x)
# for i in new:
#     for key, values in dict_.items():

# print(dict_)
# freq = {}
# for item in x:
#     if item in freq:
#         freq[item] += 1
#     else:
#         freq[item] = 1
#
# print(freq)
# for key, value in freq.items():
#     print("% d : % d" % (key, value))
from functools import reduce

p = [5,1,2,3,4,7,9]
result = list(map(lambda i: i * i, p))
print(result)

r = 81*81*81*81*9
print(r)
387420489
387420489