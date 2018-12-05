from random import randint, random
from typing import List

# TODO: Zamienic typ t_displacement na zbiór set


def first_solution(test_case: dict, t_displacement: List[List[int]],
                   available_time: int) -> [List[str], List[float], int]:  # -> List[dict['nazwa': alpha], PS]
    ti = 0  # aktualny czas
    ps = 0  # punkty satysfakcji
    last_i = 0  # nr. miejsca odwiedzonego w poprzedniej iteracji
    ans = []  # rozwiazanie
    alphas = []  # współczynniki alfa
    visited = {}  # miejsca juz odwiedzone {nr. miejsca[int]: czy byl odwiedzony[bool]}
    rand_but_not_visited = set()  # miejsca wylosowane ale nie spełniające warunków

    get_key = lambda index: list(test_case.keys())[index]  # zwraca klucz

    while available_time > ti and len(rand_but_not_visited) < len(test_case):
        i = randint(0, len(test_case))  # numer elementu rozwiązania

        if last_i != 0:
            ti += t_displacement[last_i][i]

        # test_case: dict[get_key(i)][x, y, t_otwarcia, t_zamkniecia, ps, t_maxPS]

        if i not in visited and test_case[get_key(i)][2] < ti < test_case[get_key(i)][3]:
            # sprawdzenie funkcji dopuszczalnych

            alpha = random(0, 1)

            if ti + test_case[get_key(i)][5] * alpha < available_time:
                # sprawdzenie czy dane miejse zmiescimy w dostepnym czasie

                ans[i] = get_key(i)
                alphas[i] = alpha
                ps += int(alpha * test_case[get_key(i)][4])

                visited[i] = True
                last_i = i
                rand_but_not_visited.clear()  # znalezlismy rozwiazanie, czyscimy zbior

        else:
            rand_but_not_visited.add(i)  # dodajemy rozwiazanie do zbioru

    return [ans, alphas, ps]


# TODO: funkcja next_solution(solution): dodawanie nowego elementu do rozwiązania

def next_solution(test_case: dict, t_displacement: dict[str:dict[str:int]], solution: List[str], alphas: List[float],
                  ps: int, available_time: int) -> List[dict[str: float], int]:

    rand_but_not_visited = set()

    first_elem = random.choice(solution)  # wylosowanie elementu rozwiązania
    [ti, available_time] = subtract_first_elem_from_solution(solution, alphas, t_displacement,
                                                             test_case, first_elem, available_time)

    while len(rand_but_not_visited) < len(test_case):
        second_elem = random.chice(test_case.keys())  # wylosowanie elementu dostępnych rozwiązań

        if second_elem not in solution and test_case[second_elem][2] < ti < test_case[second_elem][3]:
            alpha = random(0, 1)

            if available_time > alpha*test_case[second_elem][5]:
                ########

                ########

                rand_but_not_visited.clear()
        else:
            rand_but_not_visited = second_elem

    return [solution, alphas, ps]


def subtract_first_elem_from_solution(solution: List[str], alphas: List[float], t_displacement: dict[str:dict[str:int]],
                                      test_case: dict, first_elem: str, available_time: int) -> [int, int]:

    used_time = 0  # wykorzystany czas
    ti = 0  # aktualny czas

    for elem, alpha in solution, alphas:
        if elem == first_elem:
            if last_elem:
                used_time -= t_displacement[last_elem][elem]
                last_elem = elem
                ti = used_time
        elif last_elem == first_elem:
            used_time -= t_displacement[last_elem][elem]
            used_time += test_case[elem][5] * alpha
            last_elem = elem
        else:
            used_time += test_case[elem][5] * alpha
            last_elem = elem

        available_time -= used_time

    return [ti, available_time]