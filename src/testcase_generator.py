from pandas import DataFrame
from random import randint

print('Enter number of places:')
N = int(input())
print('Enter filename:')
filename = input()

variables = []

for i in range(6):
    variables.append([randint(0, 20) for r in range(N)])

df = DataFrame({
    'X': variables[0],
    'Y': variables[1],
    't_o': variables[2],
    't_z': variables[3],
    'PS': variables[4],
    't_maxPS': variables[5]})
df.to_excel('../testcases/' + filename + '.xls', index=False)
