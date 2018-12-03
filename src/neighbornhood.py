from random import randint, random
from typing import List


def first_solution(test_case: dict[str, tuple], t_displacement: List[List[int]],
                   available_time: int) -> List[dict[str: float], int]:  # -> List[dict['nazwa': alpha], PS]
    ti = 0  # aktualny czas
    ps = 0  # punkty satysfakcji
    last_i = 0  # nr. miejsca odwiedzonego w poprzedniej iteracji
    ans = {}  # rozwiazanie
    visited = {}  # slownik miejsc juz odwiedzonych {nr. miejsca[int]: czy byl odwiedzony[bool]}

    get_key = lambda index: list(test_case.keys())[index]  # zwraca klucz

    while available_time > ti:
        # TODO: mechanizm kontrolujacy ilosc iteracji w momencie gdy pozostały czas jest mniejszy od od minimalnego
        # TODO:(petla nieskonczona)
        i = randint(0, len(test_case))  # numer elementu rozwiązania

        if last_i != 0:
            ti += t_displacement[last_i][i]

        # test_case: dict[get_key(i)][x, y, t_otwarcia, t_zamkniecia, ps, t_maxPS]

        if i in visited and test_case[get_key(i)][2] < ti < test_case[get_key(i)][4]:
            # sprawdzenie czy element i nie był jeszcze odwiedzony oraz sprawdzenie funkcji dopuszczalnych

            alpha = random(0, 1)

            if ti + test_case[get_key(i)][5] * alpha < available_time:
                ans[get_key(i)] = alpha
                ps += int(alpha * test_case[get_key(i)][4])

                visited[i] = True
                last_i = i

    return [ans, ps]


# TODO: funkcja next_solution(solution)


def next_solution(test_case: dict[str, tuple], t_diplacement: List[List[int]],
                  solution: dict[str, float]) -> List[dict[str: float], int]:
    return 0
