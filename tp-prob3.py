import random
from itertools import permutations
import time
from itertools import chain
from itertools import zip_longest
import re

_NUMBERS = '123456789'
_OPERATIONS = '+-*/'

# region Fuerza bruta
# def generate_combinations(target=None):
#     # numbers = list(map("".join, permutations(_NUMBERS, 4)))
#     # operations = list(map("".join, permutations(_OPERATIONS, 4)))
#     numbers = permutations(_NUMBERS, 5)
#     number_combinations = {}
#     integer_combinations = {}
#     max = "0"
#     min = "0"
#     for number in numbers:
#         #Se puede pasar este iterador a un lista y no se genera en cada pasada, pero no hace ningun efecto de ejecucion. Mas bien en terminos de uso de memoria es mejor generar el iterador en cada pasada
#         operations = permutations(_OPERATIONS, 4)
#         for operation in operations:
#             expression = "".join((filter(lambda x: x != '', chain.from_iterable(
#                 zip_longest(number, operation, fillvalue='')))))
#             value = eval(expression)
#             save_value = (target is not None and value == target) or target is None
#             if save_value:
#                 number_combinations[expression] = value
#                 if value > eval(max):
#                     max = expression
#                 if value < eval(min):
#                     min = expression
#                 if abs(value - int(value)) == 0.0:
#                     integer_combinations[expression] = value
#     # print(number_combinations)
#     return number_combinations, integer_combinations, max, min

# start_time = time.time()
# combinations, integer_combinations, max, min = generate_combinations()
# print("--- %s segundos ---" % (time.time() - start_time))
# print(f'Cantidad de expresiones: {len(combinations)}')
# if max in combinations:
#     print(f'Max = {max} = {combinations[max]}')
# if min in combinations:
#     print(f'Min = {min} = {combinations[min]}')

# endregion


# region AG
# Calcular fitness
# Calcula el fitness de un individuo, el fitness en nuestro caso es simplemente la resta del valor de la expresion con el target buscado, y mientas mas cercano a 0, mejor
def get_fitness(expression: str, target_value: int):
    try:
        value = eval(expression)
        # return abs(value - target_value)
        # return 1.0 / (abs(4 - 4) + 0.000001)
        fitness = 1.0 / (abs(value - target_value) + 0.000001)
        return fitness
    except:
        return float("inf")


# Initial Population
def validate_population(expression: str):
    return all(operator in expression for operator in _OPERATIONS) and all(number in expression for number in _NUMBERS)


def build_initial_population(population_size: int = 100, target_value: int = None):
    min_correct_solutions = population_size/4
    current_correct_solutions = 0
    population_chromosomes = ""
    individuals = {}
    # Repetir mientras:
    # La poblacion aun no contenga todos los numeros y simbolos
    # El tamaNo de la poblacion sea menor al que queremos
    # No tengamos una cantidad minima de indivudos validos
    while(not validate_population(population_chromosomes) or len(individuals) < population_size or current_correct_solutions < min_correct_solutions):
        random_numbers = random.sample(_NUMBERS, 5)
        operations = list(permutations(_OPERATIONS, 4))
        random_operations_length = random.randrange(1, len(operations))
        random.shuffle(operations)
        for j in range(0, random_operations_length):
            if(len(individuals) < population_size):
                expression = "".join((filter(lambda x: x != '', chain.from_iterable(
                    zip_longest(random_numbers, operations[j], fillvalue='')))))

                #ToDo: Refactor
                valid_individual = eval(expression) == target_value
                # Si el individuo es valido lo agregamos
                if valid_individual:
                    individuals[expression] = get_fitness(
                        expression, target_value)
                    population_chromosomes = "".join(
                        set(population_chromosomes + expression))
                    current_correct_solutions += 1
                # Sino, lo agregamos si y solo aun queda espacio para los "no validos"
                # Asi garantizamos un minimo de individuos validos en la poblacion
                elif len(individuals) < (population_size - (min_correct_solutions - current_correct_solutions)):
                    individuals[expression] = get_fitness(
                        expression, target_value)
                    population_chromosomes = "".join(
                        set(population_chromosomes + expression))
    return individuals


def validate_expression(expression: str):
    unique_genes = "".join(set(expression))
    pattern = r'^[1-9]{1}[\-\+\*\/]{1}[1-9]{1}[\-\+\*\/]{1}[1-9]{1}[\-\+\*\/]{1}[1-9]{1}[\-\+\*\/]{1}[1-9]$'
    return len(unique_genes) == 9 and re.match(pattern, expression) and all(operator in unique_genes for operator in _OPERATIONS) and len([number for number in _NUMBERS if number in unique_genes]) == 5


# Ordenar la poblacion por el fitness
# El fitness es el valor de la clave en el diccionario
# population.items() nos retorna tuplas por ejemplo ('1+2-3*4/5', 0.6), por eso ordenamos en el indice [1] que es fitness de esa expresion
def order_population_by_fitness(population: list):
    return dict(sorted(population.items(), key=lambda i: i[1], reverse=True))


# Selection
# Seleccionamos en base al fitness del individuo (Ranking), recordando que el fitness de una expresion esta como valor dentro del diccionario
def select_individuals_by_ranking(population: list, new_population_size: int = 100, target_value:int = None):
    population = order_population_by_fitness(population)
    selected_individuals = list(population.keys())
    selected_individuals = selected_individuals[:new_population_size//2]
    selected_individuals = {expression : get_fitness(expression, target_value) for expression in selected_individuals}
    return selected_individuals


# Crossover
# Realizamos el cruce de los padres usando uniform crossover
# Las expresiones tienen un conjunto de 9 caracteres, serian 9 genes
# Como es aleatorio, cada cruce verificamos que la expresion sea una expresion correcta
def select_gene_from_random_parents(parents:list, gene_index:int):
    # Seleccionamos al azar el indice del que sera el padre a
    random_parent = 0 if random.randint(0, 100) < 51 else 1
    parent_a = parents[random_parent]
    parent_b = parents[abs(random_parent-1)]
    print(parent_a[gene_index], parent_b[gene_index])
    return parent_a[gene_index], parent_b[gene_index]

def cross_parents(parents: list):
    while True:  # seleccion aleatoria del padre para el gen i
        individual_a = ""
        individual_b = ""
        for gene_index in range(0, 9):
            #Debido a las restricciones del problema. Vamos a repetir la seleccion aleatoria del padre, si el gen en la posicion i de los padres, ya se encuentra en los hijos
            retries = 0
            gene_parent_a, gene_parent_b = select_gene_from_random_parents(parents, gene_index)
            while gene_parent_a in individual_a or gene_parent_b in individual_b:
                if retries > 20:
                    return parents[0], parents[1]
                gene_parent_a, gene_parent_b = select_gene_from_random_parents(parents, gene_index)
                retries += 1

            individual_a += gene_parent_a
            individual_b += gene_parent_b
            
        if validate_expression(individual_a) and validate_expression(individual_b):
            return individual_a, individual_b
    return None, None

# result1, result2 = cross_parents(["1+2-3*4/5", "1/2*4+6-7"])
# print(result1)
# print(result2)


# Mutation
# Para la mutacion seleccionamos dos caracteres al azar de la expresion y los intercambiamos. Este proceso se repetira hasta que el individuo o expresion generada, sea correcta
def mutate_population(population: dict):
    individual, individual_fitness = random.choice(list(population.items()))
    del population[individual]
    while True:
        gene_1 = random.randint(0, len(individual)-1)
        gene_2 = random.randint(0, len(individual)-1)
        while gene_2 == gene_1:
            gene_2 = random.randint(0, len(individual)-1)

        # Hacemos el cruce intercambiando los dos caracteres de la expresion
        new_individual = individual[0:gene_1] + individual[gene_2] + \
            individual[gene_1+1:gene_2] + \
            individual[gene_1] + individual[gene_2+1:]

        if validate_expression(new_individual):
            population[new_individual] = get_fitness(new_individual, _TARGET_NUMBER)
            return population


# Evaluate score
# El score sera la cantidad de individuos cuya evaluacion de la expresion es igual al target buscado
def get_population_score(population: list, target_value: int):
    population_score = len(
        list(filter(lambda ind: eval(ind) == target_value, population.keys())))
    population_score2 = 0
    for individual in population:
        if eval(individual) == target_value:
            population_score2 += 1
    return population_score


population = build_initial_population(100, 4)
# population = order_population_by_fitness(initial_population)
current_generation = 0

# Constantes
_GENERATIONS_HISTORY = {}
_POPULATION_SIZE = 100
_MAX_GENERATIONS = 100
_TARGET_SCORE = 70

###### Numero que estamos buscando #######
_TARGET_NUMBER = 4

while(current_generation < _MAX_GENERATIONS and get_population_score(population, _TARGET_NUMBER) < _TARGET_SCORE):
    # Guardamos la poblacion actual con su score
    _GENERATIONS_HISTORY[str(current_generation)] = {
        "population": list(population.keys()), "score": get_population_score(population, _TARGET_NUMBER)}

    # seleccionamos los individuos por ranking
    selected_individuals = select_individuals_by_ranking(
        population, _POPULATION_SIZE, _TARGET_NUMBER)

    # Nueva generacion vacia
    new_generation = {}
    while(len(new_generation) < _POPULATION_SIZE):
        parent_a_expression, parent_a_fitness = random.choice(
            list(selected_individuals.items()))
        parent_b_expression, parent_b_fitness = random.choice(
            list(selected_individuals.items()))
        # del selected_individuals[parent_a_expression]
        # del selected_individuals[parent_b_expression]
        children_a, children_b = cross_parents(
            [parent_a_expression, parent_b_expression])
        new_generation[children_a] = get_fitness(children_a, _TARGET_NUMBER)
        new_generation[children_b] = get_fitness(children_b, _TARGET_NUMBER)

    population = mutate_population(new_generation)
    current_generation += 1


print(population)

# endregion
