from random import randint, random
from typing import List

# TODO: funkcja next_solution(solution)

def first_solution(test_case: dict[str, tuple[6]], t_displacement: List[List[int]],
                   available_time: int) -> dict[List[str]: List[float]]:  # -> dict['nazwa': alpha, PS]
    ti = 0  # aktualny czas
    ps = 0  # punkty satysfakcji
    last_i = 0
    ans: dict[List[str]: List[float]]
    get_key = lambda index: list(test_case.keys())[index] # zwraca klucz

    while ti < available_time:

        i = randint(0, len(test_case))  # numer elementu rozwiązania
        # TODO: dodać mechanizm sprawdzający czy dane miejsce nie zostało już odwiedzone
        if last_i != 0:
            ti += t_displacement[last_i][i]

        # dict[get_key(i)][x, y, t_otwarcia, t_zamkniecia, ps, t_maxPS]

        if test_case[get_key(i)][2] < ti < test_case[get_key(i)][4]:
            alpha = random(0, 1)

            if ti + test_case[get_key(i)][5] * alpha < available_time:
                ans[get_key(i)] = alpha
                ps += int(alpha*test_case[get_key(i)][4])

    return [ans, ps]