"""
Author: Nikhil Kaushik (nk2214)
"""
import random
import sys


class RandomRestartHillClimb:
    __slots__ = 'target', 'input_number_set', 'start_state', 'local_minimum_flag', \
                'plateau_flag', 'operator_list', 'initial_expression', 'initial_best_possible', 'overall_best', \
                'best_state'

    def __init__(self):
        self.target = random.randint(1000, 9999)
        self.input_number_set = [0, 2, 8, 5, 4, 3, 1, 6, 8, 4, 3, 0, 2, 4, 5, 2, 1, 6, 8, 3, 1, 3, 4, 6, 8, 9, 7, 0, 8,
                                 1, 5, 2, 6, 8, 9, 7, 8, 3, 1, 4, 2, 1, 8, 5, 7, 4, 6, 1, 2, 3, 9, 8, 0, 7, 2, 6, 2, 3,
                                 5, 8, 4, 9, 7, 6, 1, 4, 5, 8, 9, 1, 7, 5, 2, 9, 8, 6, 1, 7, 9, 3, 5, 2, 1, 9, 4, 7, 5,
                                 6, 3, 1, 2, 7, 5, 1, 6, 2, 4, 3, 7, 1]
        self.start_state = None
        self.local_minimum_flag = False
        self.plateau_flag = False
        self.operator_list = ['+', '-', '*', '/']
        self.initial_expression = ''
        self.initial_best_possible = 0
        self.overall_best = sys.maxsize
        self.best_state = ''

    def getStartState(self):

        incorrect_initial_state_flag = True

        while incorrect_initial_state_flag:
            incorrect_initial_state_flag = False
            indexes = list(range(100))
            random.shuffle(indexes)
            self.start_state = []
            for i in indexes:
                self.start_state.append(self.input_number_set[i])

            self.initial_expression = str(self.start_state[0])
            accumulator = self.start_state[0]
            for i in range(1, len(self.start_state)):
                operator = self.operator_list[random.randint(0, 3)]
                next_number = self.start_state[i]
                if operator == '+':
                    accumulator += next_number
                elif operator == '-':
                    accumulator -= next_number
                elif operator == '*':
                    accumulator *= next_number
                else:
                    if next_number == 0:
                        incorrect_initial_state_flag = True
                        break
                    else:
                        accumulator /= next_number
                self.initial_expression = self.initial_expression + operator + str(next_number)

        self.initial_best_possible = self.target - accumulator
        print('S0', self.initial_expression)
        print('Distance From Target', self.initial_best_possible)
        print('')
        self.startRandomWalk()

    def initializeRandomWalk(self):
        print('Number Set: ', self.input_number_set)
        print('Target: ', self.target)
        print('******************************************************************************************************')
        iteration_count = 0
        while True:
            iteration_count += 1
            print('RR Iteration: ', iteration_count)
            if iteration_count > 1:
                print('Overall Best: ', self.overall_best)
                print('Overall Best State: ', self.best_state)
                print('')
            self.plateau_flag = False
            self.local_minimum_flag = False
            if self.overall_best == 0:
                print('Algorithm has converged!')
                break
            self.getStartState()
            print('***************************************************************************************************')

    def startRandomWalk(self):
        # number_of_swaps = random.randint(50, 200)
        # number_of_changes = random.randint(50, 200)
        number_of_swaps = 5
        number_of_changes = 5

        best_possible = self.initial_best_possible
        initial_expression = self.initial_expression
        while not self.plateau_flag and not self.local_minimum_flag:
            self.plateau_flag = True
            self.local_minimum_flag = True
            accumulator_list = []
            expression_list = []
            swap_count = number_of_swaps
            change_count = number_of_changes

            while swap_count > 0:
                swap_count -= 1
                i1 = random.randrange(0, len(initial_expression) - 1, 2)
                i2 = random.randrange(0, len(initial_expression) - 1, 2)
                temp_var = initial_expression[i1]
                new_expression = initial_expression[:i1] + initial_expression[i2] + initial_expression[(i1 + 1):]
                new_expression = new_expression[:i2] + temp_var + new_expression[(i2 + 1):]
                expression_list.append(new_expression)
                accumulator_list.append(self.evaluateExpression(new_expression))

            while change_count > 0:
                change_count -= 1
                i3 = random.randrange(1, len(initial_expression) - 1, 2)
                new_expression = initial_expression[:i3] + self.operator_list[
                    random.randint(0, 3)] + initial_expression[(i3 + 1):]
                expression_list.append(new_expression)
                accumulator_list.append(self.evaluateExpression(new_expression))

            best_index = -1

            for i in range(0, len(accumulator_list)):
                if 0 < accumulator_list[i] < best_possible:
                    self.plateau_flag = False
                    self.local_minimum_flag = False
                    best_possible = accumulator_list[i]
                    best_index = i

            if not self.plateau_flag and not self.local_minimum_flag:
                initial_expression = expression_list[best_index]
                print('Best State ', initial_expression)
                print('Distance from Target', best_possible)
                print('')

        if 0 < best_possible < self.overall_best:
            self.overall_best = best_possible
            self.best_state = expression_list[best_index]

    def evaluateExpression(self, expression):
        local_accumulator = int(expression[0])
        for i in range(1, len(expression) - 1, 2):
            next_number = int(expression[i + 1])
            operator = expression[i]
            if operator == '+':
                local_accumulator += next_number
            elif operator == '-':
                local_accumulator -= next_number
            elif operator == '*':
                local_accumulator *= next_number
            else:
                if next_number == 0:
                    return self.target - sys.maxsize
                else:
                    local_accumulator /= next_number
        return self.target - local_accumulator


def main():
    obj = RandomRestartHillClimb()

    obj.initializeRandomWalk()


if __name__ == '__main__':
    main()
