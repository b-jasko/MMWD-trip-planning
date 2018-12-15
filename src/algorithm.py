from math import exp
from random import random
from typing import List
from src.neighbornhood import first_solution, next_solution


def algorithm(test_case: dict, t_displacement: dict[str:dict[str:int]],
              available_time: int, t_max: int, t_min: int, len_of_sol: int) -> List[List[str], List[float], int]:

    [solution, alphas, energy] = first_solution(test_case, t_displacement, available_time)  # pierwsze rozwiązanie i
    # jego punkty
    solutions = []  # lista dobrych rozwiązań

    for t in range(t_max, t_min):
        [next_sol, alphas_next, energy_next] = next_solution(test_case, t_displacement, solution, alphas, energy,
                                                             available_time)  # następne rozwiązanie i jego punkty
        delta_e = energy_next - energy  # różnica w punktach pomiędzy rozwiązaniami

        if delta_e > 0:
            solution = next_sol
            alphas = alphas_next
            energy = energy_next
            solutions.append(solution, alphas, energy)
        elif exp(delta_e / t) > random(0, 1):
            energy = energy_next
            alphas = alphas_next
            solution = next_sol

        if len(solutions) > len_of_sol:  # sprawdź czy lista nie jest przepełniona
            del solutions[0]

    return solutions
