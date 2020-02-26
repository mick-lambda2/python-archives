import time

size = 10000000
# x = [None] * size
# time1 = time.time()
# for i in range(len(x)):
#     # NOT ACCURATE ENOUGH TO MEASURE
#     # total time is better, see that lots of iterations it changes
#     # time1 = time.time()
#     x[i] = i
#     time2 = time.time()
#     result = time2 - time1
#     print('%.12f' % result)
#     # print('init list time:', time2 - time1)
# time3 = time.time()
# result2 = time3 - time1
# print('%.6f' % result2)

result = [None] * size
y = []
time1 = time.time()
for i in range(size):
    # time1 = time.time()
    y.append(i)
    time2 = time.time()
    result[i] = time2 - time1
    # print('%.6f' % result)
time3 = time.time()
result2 = time3 - time1
print('%.6f' % result2)

print(result[25000])
print(result[100000])
print(result[200000])
print(result[300000])
print(result[400000])
print(result[500000])
print(result[600000])
print(result[700000])
print(result[800000])
print(result[900000])
print(result[999999])
