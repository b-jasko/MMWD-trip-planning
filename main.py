from src.algorithm import algorithm, import_testcase
from src.solution import OutputData
import time


if __name__ == '__main__':
    test_case = import_testcase()
    plot = OutputData([], [])
    start = time.time()
    listen = algorithm(test_case, 1, 130, 1500, 1, 1, 10, plot)
    for i in listen:
        print(i.answer)
        print(i.satisfaction_points)
    plot.plot_data()
    end = time.time()
    print('\nexecution time: ' + str(end - start))
    plot.data_to_xls()
