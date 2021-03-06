from math import exp
from random import random
from typing import List
from copy import deepcopy

from src.solution import Solution

test_case = {'Kraków': (22, 16, 0, 100, 3, 13), 'Warszawa': (27, 20, 0, 100, 5, 15), 'Lublin': (33, 19, 0, 100, 2, 10),
             'Zabrze': (20, 14, 6, 80, 1, 3), 'Frysztak': (30, 15, 0, 100, 8, 8), 'Jasło': (29, 14, 11, 60, 1, 8),
             'Krosno': (31, 14, 3, 80, 1, 7), 'Rzeszów': (32, 16, 6, 50, 2, 10), 'Dębica': (29, 16, 0, 100, 1, 9),
             'Londyn': (-30, 60, 0, 100, 10, 20), 'Zgierz': (21, 20, 0, 100, 1, 1), 'Paryż': (-25, 10, 0, 100, 10, 20)}


def algorithm(test_case: dict, velocity: int, available_time: int, t_max: int,
              t_min: int, num_of_neig: int, len_of_sol: int) -> List[Solution]:

    solution = Solution(test_case, velocity, available_time)
    current_solution = deepcopy(solution)
    best_solutions = []

    for temperature in range(t_max, t_min, -1):
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

        if difference_of_energy > 0:
            current_solution = next_solution
            best_solutions.append(next_solution)
        elif exp(difference_of_energy / temperature) > random():
            current_solution = next_solution

        if len(best_solutions) > len_of_sol:
            best_solutions.sort(key=lambda sol: sol.satisfaction_points)
            del best_solutions[0]

    return best_solutions


listen = algorithm(test_case, 1, 130, 1500, 1, 10, 10)
for i in listen:
    print(i.answer)
    print(i.satisfaction_points)
