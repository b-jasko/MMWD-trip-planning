from math import exp
from random import random
from typing import List
from src.solution import Solution


def algorithm(test_case: dict, t_displacement: dict[str:dict[str:int]],
              available_time: int, t_max: int, t_min: int, len_of_sol: int) -> List[List[str], List[float], int]:
    solution = Solution(test_case, t_displacement, available_time)
    current_solution = solution
    best_solutions = []

    for temperature in range(t_max, t_min):
        solution = current_solution
        if_not_exist = Solution.neighborhood_of_solution(solution)
        if if_not_exist == 1:
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
