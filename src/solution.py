from random import random
from random import choice as random_choice


class Solution:
    def __init__(self, test_case: dict, t_displacement: dict[str:dict[str:int]], available_time: int):
        self.answer = []
        self.alphas = []
        self.satisfaction_points = 0
        self.test_case = test_case
        self.t_displacement = t_displacement
        self.all_available_time = available_time

        current_time = 0
        last_place = 0
        visited_places = {}  # {miejsce[str]: czy byl odwiedzony[bool]}
        unacceptable_places = set()

        while available_time > current_time and len(unacceptable_places) < len(test_case):
            rand_place = random_choice(test_case.keys())
            alpha = random()  # współczynnik ilości czasu spędzonego w danym miejscu

            if last_place != 0:
                current_time += t_displacement[last_place][rand_place]
                # dodanie do aktualnego czasu czas podróży (chyba że jest to pierwsze miejsce)

            # test_case: dict[key][x, y, t_otwarcia, t_zamkniecia, ps, t_maxPS]

            if rand_place not in visited_places and test_case[rand_place][2] < current_time < test_case[rand_place][3] \
                    and current_time + test_case[rand_place][5] * alpha < available_time:
                    # sprawdzenie funkcji dopuszczalnych

                self.answer.append(rand_place)
                self.alphas.append(alpha)
                self.satisfaction_points += int(alpha * test_case[rand_place][4])

                current_time += test_case[rand_place][5] * alpha
                visited_places[rand_place] = True
                last_place = rand_place
                unacceptable_places.clear()  # znaleziono rozwiazanie, czyszczenie zbioru

            else:
                unacceptable_places.add(rand_place)  

    def neighborhood_of_solution(self):

        answer_to_rand = self.answer

        while len(answer_to_rand) != 0:
            test_case_to_rand = list(self.test_case.keys())

            place_to_override = random_choice(answer_to_rand)
            answer_to_rand.remove(place_to_override)

            [current_time, currently_available_time] = self.subtract_first_elem_from_solution(place_to_override)

            while len(test_case_to_rand) != 0:
                rand_place = random_choice(test_case_to_rand)
                test_case_to_rand.remove(rand_place)
                alpha = random()

                if rand_place not in self.answer \
                        and self.test_case[rand_place][2] < current_time < self.test_case[rand_place][3] \
                        and currently_available_time > alpha * self.test_case[rand_place][5]:

                    place_to_override_index = self.answer.index(place_to_override)

                    # wpisanie rand_place na listę rozwiązań w miejscu place_to_override
                    del self.answer[place_to_override_index]
                    self.answer.insert(place_to_override_index, rand_place)

                    # to samo dla alpha
                    del self.alphas[place_to_override_index]
                    self.alphas.insert(place_to_override_index, alpha)

                    # odjęcie punktów satysfakcji dla miejsca place_to_override oraz dodanie dla rand_place
                    self.satisfaction_points -= self.alphas[place_to_override_index] * self.test_case[place_to_override][4]
                    self.satisfaction_points += alpha * self.test_case[rand_place][4]

                    return 0  # podmienilismy rozwiazanie konczymy dzialanie funkcji
        return 1

    def subtract_first_elem_from_solution(self, first_elem: str) -> [int, int]:
        used_time = 0
        current_time = 0
        last_elem: str = '0'
        currently_available_time = self.all_available_time

        for elem, alpha in self.answer, self.alphas:
            if elem == first_elem:
                if last_elem != '0':
                    used_time -= self.t_displacement[last_elem][elem]
                    last_elem = elem
                    current_time = used_time
            elif last_elem == first_elem:
                used_time -= self.t_displacement[last_elem][elem]
                used_time += self.test_case[elem][5] * alpha
                last_elem = elem
            else:
                used_time += self.test_case[elem][5] * alpha
                last_elem = elem

            currently_available_time -= used_time

        return [current_time, currently_available_time]
