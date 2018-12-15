from random import randint, random
from typing import List


def first_solution(test_case: dict, t_displacement: dict[str:dict[str:int]],
                   available_time: int) -> [List[str], List[float], int]:  # -> List[dict['nazwa': alpha], PS]
    ti = 0  # aktualny czas
    ps = 0  # punkty satysfakcji
    last_elem = 0  # miejsce odwiedzonego w poprzedniej iteracji
    ans = []  # rozwiazanie
    alphas = []  # współczynniki alfa
    visited = {}  # miejsca juz odwiedzone {miejsce[str]: czy byl odwiedzony[bool]}
    rand_but_not_visited = set()  # miejsca wylosowane ale nie spełniające warunków

    while available_time > ti and len(rand_but_not_visited) < len(test_case):
        rand_elem: str = random.chice(test_case.keys())  # losowanie rozwiązanie
        alpha = random(0, 1)  # współczynnik ilości czasu spędzonego w danym miejscu

        if last_elem != 0:
            ti += t_displacement[last_elem][rand_elem]
            # dodanie do aktualnego czasu czas podróży (chyba że jest to pierwsze miejsce)

        # test_case: dict[key][x, y, t_otwarcia, t_zamkniecia, ps, t_maxPS]

        if rand_elem not in visited and test_case[rand_elem][2] < ti < test_case[rand_elem][3]\
                and ti + test_case[rand_elem][5] * alpha < available_time:  # sprawdzenie funkcji dopuszczalnych

                ans.append(rand_elem)
                alphas.append(alpha)
                ps += int(alpha * test_case[rand_elem][4])

                visited[rand_elem] = True
                last_elem = rand_elem
                rand_but_not_visited.clear()  # znaleziono rozwiazanie, czyszczenie zbioru

        else:
            rand_but_not_visited.add(rand_elem)  # dodanie rozwiazanie do zbioru

    return [ans, alphas, ps]


def next_solution(test_case: dict, t_displacement: dict[str:dict[str:int]], solution: List[str], alphas: List[float],
                  ps: int, available_time: int) -> List[dict[str: float], int]:

    rand_but_not_visited = set()
    rand_but_not_visited_sec = set()

    while len(rand_but_not_visited) < len(solution):

        first_elem = random.choice(solution)  # wylosowanie elementu rozwiązania (który zostanie nadpisany)

        [ti, available_time] = subtract_first_elem_from_solution(solution, alphas, t_displacement,
                                                                 test_case, first_elem, available_time)

        while len(rand_but_not_visited_sec) < len(test_case):
            second_elem = random.chice(test_case.keys())  # wylosowanie elementu spoza rozwiązania
            alpha = random(0, 1)

            if second_elem not in solution and test_case[second_elem][2] < ti < test_case[second_elem][3] \
                    and available_time > alpha * test_case[second_elem][5]:

                first_elem_index = solution.index(first_elem)  # zapisanie indeksu first_elem w solution

                solution.remove(first_elem)
                solution.insert(first_elem_index, second_elem)  # wpisanie second_elem na listę rozwiązań\

                alphas.remove(alphas[first_elem_index])  # w miejscu first_elem
                alphas.insert(first_elem_index, alpha)  # to samo dla alpha

                ps -= alphas[first_elem_index] * test_case[first_elem][4]
                ps += alpha * test_case[second_elem][4]
                # odjęcie punktów satysfakcji dla miejsca first_elem oraz dodanie dla second_elem

                return [solution, alphas, ps]  # podmienilismy rozwiazanie konczymy dzialanie funkcji
            else:
                rand_but_not_visited_sec = second_elem

        rand_but_not_visited_sec.clear()
        rand_but_not_visited = first_elem

    return [solution, alphas, ps]


def subtract_first_elem_from_solution(solution: List[str], alphas: List[float], t_displacement: dict[str:dict[str:int]],
                                      test_case: dict, first_elem: str, available_time: int) -> [int, int]:
    used_time = 0  # wykorzystany czas
    ti = 0  # aktualny czas
    last_elem: str = '0'

    for elem, alpha in solution, alphas:
        if elem == first_elem:
            if last_elem != '0':
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
