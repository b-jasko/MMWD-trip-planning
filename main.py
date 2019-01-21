from src.algorithm import algorithm, import_testcase
from src.solution import OutputData
import time


if __name__ == '__main__':
    test_case = import_testcase()
    data = OutputData([], [])
    start = time.time()
    list_of_best = algorithm(test_case=test_case,
                             velocity=30,
                             available_time=100,
                             t_max=15000,
                             t_min=100,
                             temp_ratio=0.99,
                             num_of_neig=20,
                             len_of_sol=10,
                             out_data=data,
                             prob_ratio=1000)
    for i in list_of_best:
        print('solution | alphas')
        for ans, alph in zip(i.answer, i.alphas):
            print('%8.0f | %8.2f' % (int(ans), alph))
        print('\nSatisfaction points:' + str(i.satisfaction_points) + '\n\n')
    data.plot_data()
    end = time.time()
    print('\nexecution time: ' + str(end - start))
    data.data_to_xls()
