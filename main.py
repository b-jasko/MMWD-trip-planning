from src.algorithm import algorithm, import_testcase
from src.solution import OutputData
import time


if __name__ == '__main__':
    test_case = import_testcase()
    plot = OutputData([], [])
    start = time.time()
    listen = algorithm(test_case=test_case,
                       velocity=1,
                       available_time=130,
                       t_max=15000,
                       t_min=100,
                       temp_ratio=0.99,
                       num_of_neig=1,
                       len_of_sol=10,
                       out_data=plot,
                       prob_ratio=10000)
    for i in listen:
        print('solution | alphas')
        for ans, alph in zip(i.answer, i.alphas):
            print('%8.0f | %8.2f' % (int(ans), alph))
        print('\nSatisfaction points:' + str(i.satisfaction_points) + '\n\n')
    plot.plot_data()
    end = time.time()
    print('\nexecution time: ' + str(end - start))
    plot.data_to_xls()
