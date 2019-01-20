import time
from copy import deepcopy
from math import exp
from random import random
from typing import List

from pandas import read_excel

from src.solution import Solution, OutputData


# test_case = {'Kraków': (22, 16, 0, 100, 3, 13), 'Warszawa': (27, 20, 0, 100, 5, 15), 'Lublin': (33, 19, 0, 100, 2, 10),
#              'Zabrze': (20, 14, 6, 80, 1, 3), 'Frysztak': (30, 15, 0, 100, 8, 8), 'Jasło': (29, 14, 11, 60, 1, 8),
#              'Krosno': (31, 14, 3, 80, 1, 7), 'Rzeszów': (32, 16, 6, 50, 2, 10), 'Dębica': (29, 16, 0, 100, 1, 9),
#              'Londyn': (-30, 60, 0, 100, 10, 20), 'Zgierz': (21, 20, 0, 100, 1, 1), 'Paryż': (-25, 10, 0, 100, 10, 20)}

def import_testcase() -> dict:
    print('Enter filename to import:')
    filename = input()
    df = read_excel('./testcases/' + filename + '.xlsx')
    testcase = {str(df.index[i]): tuple(df.loc[i, :]) for i in range(df.index[-1] + 1)}
    return testcase


def algorithm(test_case: dict, velocity: int, available_time: int, t_max: int, t_min: int, temp_ratio: float,
              num_of_neig: int, len_of_sol: int, out_data: OutputData, prob_ratio: float) -> List[Solution]:
    solution = Solution(test_case, velocity, available_time)
    current_solution = deepcopy(solution)
    best_solutions = []
    tmp_sp = 0

    temperature = t_max
    while temperature >= t_min:
        solution = deepcopy(current_solution)
        temp_list = []
        for iterator in range(0, num_of_neig):
            if_not_exist = Solution.neighborhood_of_solution(solution)
            temp_list.append((deepcopy(solution), if_not_exist))
            if if_not_exist:
                break
        temp_list.sort(key=lambda sol: sol[0].satisfaction_points, reverse=True)
        if_not_exist = temp_list[0][1]
        solution = temp_list[0][0]

        if if_not_exist:
            if_doesnt_work = Solution.neigh_if_few_test_cases(solution)
            if if_doesnt_work:
                best_solutions.append(current_solution)
                break

        next_solution = deepcopy(solution)

        difference_of_energy = next_solution.satisfaction_points - current_solution.satisfaction_points
        probability = exp(prob_ratio * difference_of_energy / temperature)

        if difference_of_energy > 0:
            current_solution = next_solution
            best_solutions.append(next_solution)
            out_data.add_data(temperature, current_solution.satisfaction_points)
            tmp_sp = current_solution.satisfaction_points

        elif probability > random():
            out_data.add_prob_data(temperature, probability)
            print('temperature: %5.2f  probability: %5.2f\n' % (temperature, probability))
            out_data.add_data(temperature, current_solution.satisfaction_points)
            current_solution = next_solution
            tmp_sp = current_solution.satisfaction_points

        else:
            out_data.add_data(temperature, tmp_sp)

        if len(best_solutions) >= len_of_sol:
            best_solutions.sort(key=lambda sol: sol.satisfaction_points)
            del best_solutions[0]

        temperature = (temperature * temp_ratio)

    best_solutions.sort(key=lambda sol: sol.satisfaction_points)
    return best_solutions

