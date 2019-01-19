from math import sqrt
from random import random
from random import choice as random_choice
import matplotlib.pyplot as plt
from typing import List


class Solution:
    def __init__(self, test_case: dict, velocity: int, available_time: int) -> None:
        self.answer = []
        self.alphas = []
        self.satisfaction_points = 0
        self.test_case = test_case
        self.t_displacement = count_t_displacement(test_case, velocity)
        self.all_available_time = available_time

        current_time = min(x[2] for x in test_case.values())
        last_place = 0
        places_to_rand = list(self.test_case)

        while self.all_available_time > current_time and len(places_to_rand) > 0:
            rand_place = random_choice(places_to_rand)
            places_to_rand.remove(rand_place)

            alpha = random()  # współczynnik ilości czasu spędzonego w danym miejscu

            if last_place != 0:
                current_time += self.t_displacement[last_place][rand_place]
                # dodanie do aktualnego czasu czas podróży (chyba że jest to pierwsze miejsce)

            # test_case: dict[key][x, y, t_otwarcia, t_zamkniecia, ps, t_maxPS]
            if self.test_case[rand_place][2] <= current_time < self.test_case[rand_place][3] and current_time + \
                    self.test_case[rand_place][5] * alpha < self.all_available_time:
                # sprawdzenie funkcji dopuszczalnych

                self.answer.append(rand_place)
                self.alphas.append(alpha)
                places_to_rand = list(set(test_case)-set(self.answer))

                current_time += self.test_case[rand_place][5] * alpha
                last_place = rand_place
        self.count_satisfaction_points()

    def count_satisfaction_points(self) -> None:
        points = 0
        for place in self.answer:
            points += round(self.alphas[self.answer.index(place)] * self.test_case[place][4])
        self.satisfaction_points = points

    def neighborhood_of_solution(self) -> bool:

        answer_to_rand = self.answer.copy()

        while len(answer_to_rand) > 0:
            test_case_to_rand = list(self.test_case.keys())

            place_to_override = random_choice(answer_to_rand)
            answer_to_rand.remove(place_to_override)

            [current_time, currently_available_time] = self.get_current_time(place_to_override, self.all_available_time)

            while len(test_case_to_rand) > 0:
                rand_place = random_choice(test_case_to_rand)
                test_case_to_rand.remove(rand_place)
                place_to_override_index = self.answer.index(place_to_override)

                alpha = random()

                def is_proper() -> bool:
                    if place_to_override_index == len(self.answer) - 1:
                        isproper = rand_place not in self.answer \
                                   and self.test_case[rand_place][2] <= current_time + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][rand_place] \
                                   and current_time + self.t_displacement[self.answer[place_to_override_index - 1]][
                                       rand_place] + \
                                   self.test_case[rand_place][5] * alpha < self.test_case[rand_place][3] \
                                   and currently_available_time > alpha * self.test_case[rand_place][5] + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][rand_place]
                    elif place_to_override_index == 0:
                        isproper = rand_place not in self.answer \
                                   and self.test_case[rand_place][2] <= current_time \
                                   and self.test_case[rand_place][5] * alpha < self.test_case[rand_place][3] \
                                   and currently_available_time > alpha * self.test_case[rand_place][5] + \
                                   self.t_displacement[self.answer[place_to_override_index + 1]][rand_place]

                    else:
                        isproper = rand_place not in self.answer \
                                   and self.test_case[rand_place][2] <= current_time + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][rand_place] \
                                   and current_time + self.t_displacement[self.answer[place_to_override_index - 1]][
                                       rand_place] + \
                                   self.test_case[rand_place][5] * alpha < self.test_case[rand_place][3] \
                                   and currently_available_time > alpha * self.test_case[rand_place][5] + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][rand_place] + \
                                   self.t_displacement[self.answer[place_to_override_index + 1]][rand_place]

                    return isproper

                if is_proper() and rand_place not in self.answer:
                    # wpisanie rand_place na listę rozwiązań w miejscu place_to_override
                    del self.answer[place_to_override_index]
                    self.answer.insert(place_to_override_index, rand_place)

                    # to samo dla alpha
                    del self.alphas[place_to_override_index]
                    self.alphas.insert(place_to_override_index, alpha)

                    # odjęcie punktów satysfakcji dla miejsca place_to_override oraz dodanie dla rand_place
                    self.count_satisfaction_points()

                    self.add_place_to_solution()

                    return False  # podmienilismy rozwiazanie konczymy dzialanie funkcji
        return True

    def neigh_if_few_test_cases(self) -> bool:
        answer_to_rand = self.answer.copy()

        while len(answer_to_rand) > 0:
            test_case_to_rand = list(self.answer)

            place_to_override = random_choice(answer_to_rand)
            answer_to_rand.remove(place_to_override)
            place_to_override_index = self.answer.index(place_to_override)

            if place_to_override_index == 0 or place_to_override_index == len(self.answer) - 1:
                continue

            [current_time_1, currently_available_time] = self.get_current_time(place_to_override,
                                                                               self.all_available_time)

            while len(test_case_to_rand) > 0:
                rand_place = random_choice(test_case_to_rand)
                rand_place_index = self.answer.index(rand_place)
                test_case_to_rand.remove(rand_place)
                if rand_place == place_to_override \
                        or (rand_place_index == 0 or rand_place_index == len(self.answer) - 1) \
                        or place_to_override_index+1 == rand_place_index \
                        or place_to_override_index-1 == rand_place_index:
                    continue


                [current_time_2, currently_available_time] = self.get_current_time(rand_place, self.all_available_time)
                currently_available_time += self.test_case[place_to_override][5] * self.alphas[place_to_override_index]\
                + self.t_displacement[self.answer[place_to_override_index-1]][self.answer[place_to_override_index]]\
                + self.t_displacement[self.answer[place_to_override_index+1]][self.answer[place_to_override_index]]

                alpha_1 = random()
                alpha_2 = random()

                def is_proper() -> bool:
                    if place_to_override_index == len(self.answer) - 1:
                        isproper = currently_available_time >= self.t_displacement[self.answer[place_to_override_index-1]][self.answer[place_to_override_index]] +\
                            self.test_case[place_to_override][5]*alpha_1 + \
                            self.t_displacement[self.answer[rand_place_index - 1]][self.answer[rand_place_index]] + \
                            self.test_case[rand_place][5] * alpha_1 + \
                            self.t_displacement[self.answer[rand_place_index + 1]][self.answer[rand_place_index]] \
                            and self.test_case[place_to_override][2] <= current_time_2 + self.t_displacement[self.answer[rand_place_index-1]][self.answer[place_to_override_index]] \
                            and self.test_case[place_to_override][3] >= current_time_2 + self.t_displacement[self.answer[rand_place_index-1]][self.answer[place_to_override_index]] + self.t_displacement[self.answer[rand_place_index +1]][self.answer[place_to_override_index]] \
                            and self.test_case[rand_place][2] <= current_time_1 + self.t_displacement[self.answer[place_to_override_index-1]][self.answer[rand_place_index]] \
                            and self.test_case[rand_place][3] >= current_time_1 + self.t_displacement[self.answer[place_to_override_index-1]][self.answer[rand_place_index]]

                    elif place_to_override_index == 0:
                        isproper = currently_available_time >= \
                            self.test_case[place_to_override][5]*alpha_1 + \
                            self.t_displacement[self.answer[place_to_override_index+1]][self.answer[place_to_override_index]] + \
                            self.t_displacement[self.answer[rand_place_index - 1]][self.answer[rand_place_index]] + \
                            self.test_case[rand_place][5] * alpha_1 + \
                            self.t_displacement[self.answer[rand_place_index + 1]][self.answer[rand_place_index]] \
                            and self.test_case[place_to_override][2] <= current_time_2 + self.t_displacement[self.answer[rand_place_index-1]][self.answer[place_to_override_index]] \
                            and self.test_case[place_to_override][3] >= current_time_2 + self.t_displacement[self.answer[rand_place_index-1]][self.answer[place_to_override_index]] + self.t_displacement[self.answer[rand_place_index +1]][self.answer[place_to_override_index]] \
                            and self.test_case[rand_place][2] <= current_time_1 \
                            and self.test_case[rand_place][3] >= current_time_1 + self.t_displacement[self.answer[place_to_override_index +1]][self.answer[rand_place_index]]

                    elif rand_place_index == len(self.answer) - 1:
                        isproper = currently_available_time >= \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][self.answer[place_to_override_index]] + \
                                   self.test_case[place_to_override][5] * alpha_1 + \
                                   self.t_displacement[self.answer[place_to_override_index + 1]][self.answer[place_to_override_index]] + \
                                   self.t_displacement[self.answer[rand_place_index - 1]][self.answer[rand_place_index]] + \
                                   self.test_case[rand_place][5] * alpha_1 \
                                   and self.test_case[place_to_override][2] <= current_time_2 + \
                                   self.t_displacement[self.answer[rand_place_index - 1]][self.answer[place_to_override_index]] \
                                   and self.test_case[place_to_override][3] >= current_time_2 + \
                                   self.t_displacement[self.answer[rand_place_index - 1]][self.answer[place_to_override_index]] \
                                   and self.test_case[rand_place][2] <= current_time_1 + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][self.answer[rand_place_index]] \
                                   and self.test_case[rand_place][3] >= current_time_1 + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][self.answer[rand_place_index]] + \
                                   self.t_displacement[self.answer[place_to_override_index + 1]][self.answer[rand_place_index]]

                    elif rand_place_index == 0:
                        isproper = currently_available_time >= \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][self.answer[place_to_override_index]] + \
                                   self.test_case[place_to_override][5] * alpha_1 + \
                                   self.t_displacement[self.answer[place_to_override_index + 1]][self.answer[place_to_override_index]] + \
                                   self.test_case[rand_place][5] * alpha_1 + \
                                   self.t_displacement[self.answer[rand_place_index + 1]][self.answer[rand_place_index]] \
                                   and self.test_case[place_to_override][2] <= current_time_2 \
                                   and self.test_case[place_to_override][3] >= current_time_2 + \
                                   self.t_displacement[self.answer[rand_place_index + 1]][self.answer[place_to_override_index]] \
                                   and self.test_case[rand_place][2] <= current_time_1 + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][self.answer[rand_place_index]] \
                                   and self.test_case[rand_place][3] >= current_time_1 + \
                                   self.t_displacement[self.answer[place_to_override_index - 1]][self.answer[rand_place_index]] + \
                                   self.t_displacement[self.answer[place_to_override_index + 1]][self.answer[rand_place_index]]

                    else:
                        isproper = currently_available_time >= self.t_displacement[self.answer[place_to_override_index-1]][self.answer[place_to_override_index]] + self.test_case[place_to_override][5]*alpha_1 + self.t_displacement[self.answer[place_to_override_index+1]][self.answer[place_to_override_index]] + self.t_displacement[self.answer[rand_place_index - 1]][self.answer[rand_place_index]] + self.test_case[rand_place][5] * alpha_1 + self.t_displacement[self.answer[rand_place_index + 1]][self.answer[rand_place_index]] and self.test_case[place_to_override][2] <= current_time_2 + self.t_displacement[self.answer[rand_place_index-1]][self.answer[place_to_override_index]] and self.test_case[place_to_override][3] >= current_time_2 + self.t_displacement[self.answer[rand_place_index-1]][self.answer[place_to_override_index]] + self.t_displacement[self.answer[rand_place_index +1]][self.answer[place_to_override_index]] and self.test_case[rand_place][2] <= current_time_1 + self.t_displacement[self.answer[place_to_override_index-1]][self.answer[rand_place_index]] and self.test_case[rand_place][3] >= current_time_1 + self.t_displacement[self.answer[place_to_override_index-1]][self.answer[rand_place_index]] + self.t_displacement[self.answer[place_to_override_index +1]][self.answer[rand_place_index]]
                    return isproper

                if is_proper():
                    rand_place_index = self.answer.index(rand_place)

                    # zamiana miejscami rand_place i place_to_override na liście rozwiązań
                    del self.answer[place_to_override_index]
                    self.answer.insert(place_to_override_index, rand_place)

                    del self.answer[rand_place_index]
                    self.answer.insert(rand_place_index, place_to_override)

                    # to samo dla alpha
                    del self.alphas[place_to_override_index]
                    self.alphas.insert(place_to_override_index, alpha_1)

                    del self.alphas[rand_place_index]
                    self.alphas.insert(rand_place_index, alpha_2)

                    # odjęcie punktów satysfakcji dla miejsca place_to_override oraz dodanie dla rand_place
                    self.count_satisfaction_points()

                    self.add_place_to_solution()

                    return False  # podmienilismy rozwiazanie konczymy dzialanie funkcji
        return True

    def get_current_time(self, place: str, all_available_time: int) -> [int, int]:
        used_time = 0
        current_time = 0
        last_elem: str = '0'
        last_alpha: str = '0'
        currently_available_time = all_available_time

        for elem, alpha in zip(self.answer, self.alphas):

            if elem == place:
                if last_elem != '0':
                    used_time += self.test_case[last_elem][5] * last_alpha
                    current_time = used_time
            elif last_elem == place:
                pass
            else:
                if last_elem != '0':
                    used_time += self.test_case[last_elem][5] * last_alpha
                    used_time += self.t_displacement[last_elem][elem]
            last_elem = elem
            last_alpha = alpha
        if place != last_elem:
            used_time += self.test_case[last_elem][5] * last_alpha
        currently_available_time -= used_time

        return [current_time, currently_available_time]

    def add_place_to_solution(self):
        unused_places = list(set(self.test_case.keys()) - set(self.answer))
        while len(unused_places) > 0:
            [current_time, currently_available_time] = self.get_current_time(self.answer[len(self.answer)-1], self.all_available_time)
            current_time += self.t_displacement[self.answer[len(self.answer)-2]][self.answer[len(self.answer)-1]] + \
                            self.test_case[self.answer[len(self.answer)-1]][5] * self.alphas[len(self.answer)-1]
            currently_available_time = self.all_available_time - current_time

            rand_place = random_choice(unused_places)
            unused_places.remove(rand_place)
            alpha = random()

            if currently_available_time >= current_time + self.t_displacement[self.answer[len(self.answer)-1]][rand_place] + \
                self.test_case[rand_place][5] * alpha and \
                self.test_case[rand_place][2] <= current_time + self.t_displacement[self.answer[len(self.answer)-1]][rand_place] and \
                self.test_case[rand_place][3] >= current_time + self.t_displacement[self.answer[len(self.answer)-1]][rand_place] + self.test_case[rand_place][5] * alpha:
                self.answer.append(rand_place)
                self.alphas.append(alpha)
                self.count_satisfaction_points()
                unused_places = list(set(self.test_case.keys()) - set(self.answer))


def count_t_displacement(test_case: dict, velocity: int) -> dict:
    t_displacements = {}

    for start in test_case:
        temp_dict = {}
        for finish in test_case:
            if finish != start:
                x_displacement = test_case[finish][0] - test_case[start][0]
                y_displacement = test_case[finish][1] - test_case[start][1]
                displacement = sqrt(pow(x_displacement, 2) + pow(y_displacement, 2))
                t_displacement = int(displacement / velocity)
                temp_dict[finish] = t_displacement
        t_displacements[start] = temp_dict

    return t_displacements


class PlotSpIterations:
    def __init__(self, iterations, sp):
        self.sp: List[int] = sp
        self.iterations: List[int] = iterations

    def add_data(self, iterations, sp):
        self.sp.append(sp)
        self.iterations.append(iterations)

    def plot_data(self):
        plt.plot(self.iterations, self.sp)
