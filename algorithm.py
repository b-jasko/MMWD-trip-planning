from math import exp
from random import random
from typing import List
from src.neighbornhood import first_solution


def algorithm(test_case: dict[str, tuple[6]], t_displacement: List[List[int]],
                   available_time: int, t_max: int, t_min: int, len_of_sol: int) -> List[dict[List[str]: List[float]]]:

    [solution, e_c] = first_solution(test_case, t_displacement, available_time)  # pierwsze rozwiązanie i jego punkty
    solutions = List[solution]                          # lista dobrych rozwiązań

    for t in  range(t_max, t_min):
        [next_solution, e_n] = next_solution(solution)  # następne rozwiązanie i jego punkty
        delta_e = e_n - e_c                             # różnica w punktach pomiędzy rozwiązaniami

        if delta_e > 0:
            solution = next_solution
            solutions.append(solution)
        elif exp(delta_e/t) > random(0,1):
            solution = next_solution

        if len(solutions) > len_of_sol:                # sprawdź czy lista nie jest przepełniona
            del solutions[0]

    return solutions
