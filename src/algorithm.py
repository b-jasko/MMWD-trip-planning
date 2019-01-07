from math import exp
from random import random
from typing import List

from src.solution import Solution, count_t_displacement

test_case = {'Kraków': (22, 15, 0, 100, 3, 13), 'Warszawa': (25, 20, 0, 100, 5, 15), 'Lublin': (27, 19, 0, 100, 2, 10)}


def algorithm(test_case: dict, velocity: int, available_time: int, t_max: int,
              t_min: int, len_of_sol: int) -> List[Solution]:

    solution = Solution(test_case, velocity, available_time)
    current_solution = solution
    best_solutions = []

    for temperature in range(t_min, t_max):
        solution = current_solution
        if_not_exist = Solution.neighborhood_of_solution(solution)
        if if_not_exist == 1:
            best_solutions.append(current_solution)
            if_doesnt_work = Solution.neigh_if_few_test_cases(solution)
            if if_doesnt_work == 1:
                break

        next_solution = solution

        difference_of_energy = next_solution.satisfaction_points - current_solution.satisfaction_points

        if difference_of_energy > 0:
            current_solution = next_solution
            best_solutions.append(next_solution)
        elif exp(difference_of_energy / temperature) > random():
            current_solution = next_solution

        if len(best_solutions) > len_of_sol:
            del best_solutions[0]

    return best_solutions


listen = algorithm(test_case, 0.5, 1000, 1500, 10, 10)
for i in listen:
    print(i.answer)
