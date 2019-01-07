from pandas import DataFrame
from random import randint, sample

print('Enter number of places:')
N = int(input())
print('Enter filename:')
filename = input()

X = []
Y = []
t_o = []
t_z = []
PS = [randint(1, 10) for r in range(N)]
t_maxPS = []

max_distance = 20
max_closing_time = 40
places = []
i = 0

while i < N:
    x = randint(0, max_distance)
    y = randint(0, max_distance)
    pair = [x, y]
    if pair not in places:
        places.append(pair)
        X.append(x)
        Y.append(y)
        i += 1

for i in range(N):
    temp = sorted(sample(range(1, max_closing_time), 2))
    t_o.append(temp[0])
    t_z.append(temp[1])
    t_maxPS.append(randint(1, temp[1] - temp[0]))

df = DataFrame({
    'X': X,
    'Y': Y,
    't_o': t_o,
    't_z': t_z,
    'PS': PS,
    't_maxPS': t_maxPS})
df.to_excel('../testcases/' + filename + '.xls', index=False)


