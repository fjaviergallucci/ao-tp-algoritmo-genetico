from itertools import permutations
import time
from itertools import chain
from itertools import zip_longest


_NUMBERS = '123456789'
_OPERATIONS = '+-*/'

# region Fuerza bruta
def generate_combinations(target=None):
    # numbers = list(map("".join, permutations(_NUMBERS, 4)))
    # operations = list(map("".join, permutations(_OPERATIONS, 4)))
    numbers = permutations(_NUMBERS, 5)
    number_combinations = {}
    integer_combinations = {}
    max = "0"
    min = "0"
    for number in numbers:
        #Se puede pasar este iterador a un lista y no se genera en cada pasada, pero no hace ningun efecto de ejecucion. Mas bien en terminos de uso de memoria es mejor generar el iterador en cada pasada
        operations = permutations(_OPERATIONS, 4)
        for operation in operations:
            expression = "".join((filter(lambda x: x != '', chain.from_iterable(
                zip_longest(number, operation, fillvalue='')))))
            value = eval(expression)
            save_value = (target is not None and value == target) or target is None
            if save_value:
                number_combinations[expression] = value
                if value > eval(max):
                    max = expression
                if value < eval(min):
                    min = expression
                if abs(value - int(value)) == 0.0:
                    integer_combinations[expression] = value
    # print(number_combinations)
    return number_combinations, integer_combinations, max, min


start_time = time.time()
combinations, integer_combinations, max, min = generate_combinations(4)
print("--- %s segundos ---" % (time.time() - start_time))
print(f'Cantidad de expresiones: {len(combinations)}')
if max in combinations:
    print(f'Max = {max} = {combinations[max]}')
if min in combinations:
    print(f'Min = {min} = {combinations[min]}')

# endregion


# #region AG
# def validate_expression(expression : str):
#     return all(operator in expression for operator in _OPERATIONS) and any(number in expression for number in _NUMBERS) == 4


# def build_initial_population():
#     population_length = 100
#     individuals = []
#     for i in range(0, 100):
#         random_numbers = random.choice(_NUMBERS, k=4)

# #endregion
