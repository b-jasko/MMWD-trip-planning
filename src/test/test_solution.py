import unittest

from src.solution import Solution
from src.solution import count_t_displacement
from src.solution import PlotSpIterations

temp_test_case = {'Kraków': (22, 15, 0, 100, 3, 13), 'Warszawa': (25, 15, 0, 100, 5, 15),
                  'Lublin': (27, 15, 0, 100, 2, 10)}

temp_test_case_2 = {'Kraków': (22, 15, 0, 100, 3, 30), 'Warszawa': (25, 15, 0, 100, 5, 15),
                    'Lublin': (27, 15, 0, 100, 2, 20)}


class TestSolution(unittest.TestCase):
    def test_init(self):
        solution = Solution(temp_test_case, 10, 100)

        self.assertEqual(len(temp_test_case), len(solution.answer))
        self.assertEqual(len(temp_test_case), len(solution.alphas))
        self.assertEqual(100, solution.all_available_time)
        self.assertEqual(len(temp_test_case), len(solution.t_displacement))
        self.assertEqual(temp_test_case, solution.test_case)

    def test_count_satisfaction_points(self):

        solution = Solution(temp_test_case, 10, 100)

        solution.answer = list(temp_test_case)
        solution.alphas = [1, 1, 1]
        Solution.count_satisfaction_points(solution)

        self.assertEqual(10, solution.satisfaction_points)

    def test_get_current_time(self):
        solution = Solution(temp_test_case, 1, 100)
        solution.answer = list(temp_test_case)
        solution.alphas = [1, 1, 1]

        ans = Solution.get_current_time(solution, 'Kraków', solution.all_available_time)
        [current_time, currently_available_time] = ans

        self.assertEqual(0, current_time)
        self.assertEqual(73, currently_available_time)  # 100-[Warszawa(15)+trasa(2)+Lublin(10)] = 73

        # ---------------------------------------------------

        solution = Solution(temp_test_case, 1, 100)
        solution.answer = list(temp_test_case)
        solution.alphas = [1, 1, 1]

        ans = Solution.get_current_time(solution, 'Lublin', solution.all_available_time)
        [current_time, currently_available_time] = ans

        self.assertEqual(31, current_time)
        self.assertEqual(69, currently_available_time)  # 100-[Krakow(13)+trasa(3)+Warszawa(15)] = 69

        # ---------------------------------------------------

        solution = Solution(temp_test_case_2, 1, 100)
        solution.answer = list(temp_test_case)
        solution.alphas = [1, 1, 1]

        ans = Solution.get_current_time(solution, 'Warszawa', solution.all_available_time)
        [current_time, currently_available_time] = ans

        self.assertEqual(30, current_time)
        self.assertEqual(50, currently_available_time)  # 100-[Kraków(30)+trasa(2)+Lublin(20)] = 50

    def test_count_t_displacement(self):
        t_displacement = count_t_displacement(temp_test_case, 1)

        self.assertEqual(3, t_displacement['Kraków']['Warszawa'])
        self.assertEqual(5, t_displacement['Kraków']['Lublin'])
        self.assertEqual(2, t_displacement['Lublin']['Warszawa'])


class TestPsIterations(unittest.TestCase):
    def test_init(self):
        test = PlotSpIterations([1, 2, 3], [1, 2, 1])
        self.assertEqual(test.iterations, [1, 2, 3])
        self.assertEqual(test.ps, [1, 2, 1])

    def test_add_data(self):
        test = PlotSpIterations([1, 2, 3], [1, 2, 1])
        test.add_data(5, 7)
        self.assertEqual(test.iterations, [1, 2, 3, 5])
        self.assertEqual(test.ps, [1, 2, 1, 7])


if __name__ == '__main__':
    unittest.main()
