from math import exp
from random import random
from typing import List
from src.neighbornhood import first_solution, next_solution


def algorithm(test_case: dict[str, tuple], t_displacement: List[List[int]],
              available_time: int, t_max: int, t_min: int, len_of_sol: int) -> List[dict[List[str]: List[float]]]:

    [solution, energy_first] = first_solution(test_case, t_displacement, available_time)  # pierwsze rozwiązanie i
    # jego punkty
    solutions = []  # lista dobrych rozwiązań

    for t in range(t_max, t_min):
        [next_sol, energy_next] = next_solution(solution)  # następne rozwiązanie i jego punkty
        delta_e = energy_next - energy_first  # różnica w punktach pomiędzy rozwiązaniami

        if delta_e > 0:
            solution = next_sol
            energy_first = energy_next
            solutions.append(solution)
        elif exp(delta_e / t) > random(0, 1):
            energy_first = energy_next
            solution = next_sol

        if len(solutions) > len_of_sol:  # sprawdź czy lista nie jest przepełniona
            del solutions[0]

    return solutions
