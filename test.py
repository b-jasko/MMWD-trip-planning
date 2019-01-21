from src.algorithm import algorithm, import_testcase
from src.solution import OutputData
import time


temp_test_case = {'1': (22, 15, 0, 100, 3, 13), '2': (25, 15, 0, 100, 5, 15),
                  '3': (27, 15, 0, 100, 2, 10), '4': (20, 14, 6, 80, 1, 3),
                  '5': (30, 15, 0, 100, 8, 8), '6': (29, 14, 11, 60, 1, 8)}

data = OutputData([], [], './data/test_sp.xlsx', './data/test_prob.xlsx')
start = time.time()
[best_solutions, solutions] = algorithm(test_case=temp_test_case,
                           velocity=1,
                           available_time=130,
                           t_max=1000,
                           t_min=100,
                           temp_ratio=0.2,
                           num_of_neig=10,
                           len_of_sol=10,
                           out_data=data,
                           prob_ratio=10000)



for i in solutions:
    print('solution | alphas')
    for ans, alph in zip(i.answer, i.alphas):
        print('%8.0f | %8.2f' % (int(ans), alph))
    print('\nSatisfaction points:' + str(i.satisfaction_points) + '\n\n')
data.plot_data()
end = time.time()
print('\nexecution time: ' + str(end - start))
data.data_to_xls()


for i in best_solutions:
    print('solution | alphas')
    for ans, alph in zip(i.answer, i.alphas):
        print('%8.0f | %8.2f' % (int(ans), alph))
    print('\nSatisfaction points:' + str(i.satisfaction_points) + '\n\n')
data.plot_data()
end = time.time()
print('\nexecution time: ' + str(end - start))
data.data_to_xls()