import pandas as pd
import s5code
import numpy
objs5=s5code.module()
objs5.s5comm()
# filename="outpath.csv"
readCSV = pd.read_csv('path.csv', sep=',', header=None, dtype=str)
# store=numpy.zeros((100,13))
points = readCSV.values
# print(points)

# print ("Sending points")
for y in range(0, 400):
    for x in range(0, 6):
        objs5.s5(points[y][x])
#
print ("Points Sent")
# for y in range(0, 100):
#     for x in range(0, 6):
#         store[y][x]=points[y][x]
#         points[y][x]=float(objs5.s5read())
#         store[y][x + 6] = points[y][x]
# print ("Receiving time")
# for y in range(0, 100):
#     points[y][0]=float(objs5.s5read())
#     store[y][12] = points[y][0]
# numpy.savetxt(filename,store,delimiter=',')
# print ("Points saved in bpoints.csv")