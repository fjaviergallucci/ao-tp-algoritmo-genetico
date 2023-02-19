import random
from itertools import permutations
import time
from itertools import chain
from itertools import zip_longest
import re
import copy


""" Problemas a resolver
Fuerza bruta:
1: Dado un número, generar una expresión combinando números y operaciones
2: Generar todas las posibles permutaciones y:
    2.1: Buscar max
    2.2: Buscar min
    2.3: Valores enteros intermedios

Otros algoritmos no fuerza bruta:
1: Dado un número, generar una expresión combinando números y operaciones
2: Generar todas las posibles permutaciones y:
    2.1: Buscar max
    2.2: Buscar min
    2.3: Valores enteros intermedios

Restricciones:
-Estructura de las expresiones: 1+2-3*4/5
-No se pueden repetir los números
-No se pueden repetir las operaciones
"""


# region globals
"""Region de funciones y constantes"""
_NUMBERS = '123456789'
_OPERATIONS = '+-*/'
_EXPRESSION_PATTERN = r'^[1-9]{1}[\-\+\*\/]{1}[1-9]{1}[\-\+\*\/]{1}[1-9]{1}[\-\+\*\/]{1}[1-9]{1}[\-\+\*\/]{1}[1-9]$'


def generate_number_yield():
    """Genera todas las posibles permutaciones de números

    Returns:
      Yield con el número o permutación generada.
    """
    for number in permutations(_NUMBERS, 5):
        yield number


def generate_operations_yield():
    """Esta función generará todas las posibles permutaciones de operadores

    Returns:
      Yield con la permutación generada de los operadores
    """
    for operation in permutations(_OPERATIONS, 4):
        yield operation


def generate_expresion(number: str, operators: str):
    """Genera la expresión dado los números y los operadores

    La función recorre ambos strings y genera una combinación de ambos respetando el orden y la estructura esperada

    Args:
      number: Permutación de los números, por ejemplo "37586"
      operators: Permutación de los operadores, por ejemplo: "+/*-"

    Returns:
      Expression generada
    """
    return "".join((filter(lambda x: x != '', chain.from_iterable(
        zip_longest(number, operators, fillvalue='')))))


def expression_is_valid(expression: str):
    """Valida una expresión dada que cumpla con las reglas

    Args:
        expression: Expresión a ser evaluada

    Returns:
        True si la expresión es correcta y cumple con las reglas
    """
    unique_genes = "".join(set(expression))
    length_valid = len(unique_genes) == 9
    pattern_valid = re.match(_EXPRESSION_PATTERN, expression)
    operators_valid = all(operator in unique_genes for operator in _OPERATIONS)
    numbers_valid = len(
        [number for number in _NUMBERS if number in unique_genes]) == 5
    return length_valid and pattern_valid and operators_valid and numbers_valid


# endregion


# region Fuerza bruta
"""
Fuerza bruta
1: Dado un número, generar una expresion combinando numeros y operaciones
2: Generar todas las posibles combinaciones y:
    2.1: Buscar max
    2.2: Buscar min
    2.3: Valores enteros intermedios
"""

def find_expressions(target: int = None):
    """Funcion principal que genera todas las permutaciones o expresiones posibles y devuelve:

    Args:
      target: El numero para el cual se desan generar expresiones. Si no se pasa el target, se generaran todas las posibles permutaciones. Si se define el target, se devolveran solo las permutaciones que al ser evaluadas den ese numero

    Returns:
      number_permutations: Todas las permutaciones encontradas
      integer_permutations: Permutaciones cuya evaluaciones dan numeros enteros
      max: Permutacion que devuelve valor maximo
      min: Permutacion que devuelve valor minimo
    """
    number_permutations = {}
    integer_permutations = {}
    max = "0"
    min = "0"
    # Como las permutaciones de numeros son cientos de miles, usamos un generador para ahorrar memoria y tiempo de procesamiento
    for number in generate_number_yield():
        # En el caso particulas de las operaciones se puede pasar este generador a un lista. Pero no hace ninguna diferencia en recursos. Mejor seguir usando generadores
        for operation in generate_operations_yield():
            # Como ya tenemos todas las posibles permutaciones de operaciones. Lo que hay que hacer es jutnar el numero generado con el orden de los operadores y asi se obtienen todas las permutacioens de un numero con los operadores
            expression = generate_expresion(number, operation)
            value = eval(expression)

            # Si estamos buscando un target y la expresion generada lo cumple, la devolvemos, sino, continuamos
            if target is not None and value == target:
                return {expression: value}, None, None, None
            elif target is None:
                number_permutations[expression] = value
                # Verificamos si es el nuevo maximo
                if value > eval(max):
                    max = expression
                # Verificamos si es el nuevo minimo
                if value < eval(min):
                    min = expression
                # Lo guardamos si el resultado de la expresion es entero
                if abs(value - int(value)) == 0.0:
                    integer_permutations[expression] = value
    # print(number_combinations)
    return number_permutations, integer_permutations, max, min


#Buscar expresiones para el numero
_NUMBER_TO_SEARCH = 350
start_time = time.time()
expressions, _, _, _ = find_expressions(_NUMBER_TO_SEARCH)
print("--- %s segundos ---" % (time.time() - start_time))
print(f'Expresion encontrada: {expressions}')


# #Encontrar max, min, enteros intermedios
# start_time = time.time()
# expressions, integer_expressions, max, min = find_expressions()
# print("--- %s segundos ---" % (time.time() - start_time))
# print(f'Cantidad de expresiones: {len(expressions)}')
# if max in expressions:
#     print(f'Max = {max} = {expressions[max]}')
# if min in expressions:
#     print(f'Min = {min} = {expressions[min]}')
# print(f'Cantidad de expresiones con valores enteros: {len(integer_expressions)}')
# print(f'Primeras 10 expresiones con valores enteros encontradas:')
# count = 0
# for expresion in expressions:
#     if count <= 10:
#         count += 1
#         print(expresion)

# print()

# endregion


# region AG
"""
Algoritmo genético para resolver:
1: Dado un número, generar una expresion combinando números y operaciones
2: Generar todas las posibles permutaciones y:
    2.1: Buscar max
    2.2: Buscar min
    2.3: Valores enteros intermedios
"""


def get_individuals_with_integer_fitness(population: dict):
    """Devuelve los individuos cuyo fitness es entero

    Calcula el fitness de un individuo, el fitness en nuestro caso es simplemente la evaluación de la expresion

    Args:
      individual: Expresión a evaluar

    Returns:
      El fitness del individuo
    """
    individuals = dict(filter(lambda i: abs(
        i[1] - int(i[1])) == 0.0, population.items()))
    return individuals


def get_fitness(individual: str):
    """Calcular fitness

    Calcula el fitness de un individuo, el fitness en nuestro caso es simplemente la evaluación de la expresion

    Args:
      individual: Expresión a evaluar

    Returns:
      El fitness del individuo
    """
    try:
        return eval(individual)
    except:
        return 0


def population_is_valid(expression: str):
    """Valida la población

    Valida que los genes que poseen todos los individuos de la población, tienen todos los números y operadores al menos una vez

    Args:
      expression: String que contiene todos los genes sin repetir de todos los individuos de la población a evaluar

    Returns:
      Verdadero si la expresion contiene todos los números y operadores definidos
    """
    return all(operator in expression for operator in _OPERATIONS) and all(number in expression for number in _NUMBERS)


def get_population_score(population: dict):
    """Calcula el score de la población

    El score viene dado por la suma total de los valores absolutos de los fitness de cada individuo

    Args:
      population: Población

    Returns:
        Suma de los fitness
    """
    return sum(map(abs, population.values()))


def find_individuals_by_fitness(population: dict, target_value: int):
    """Busca individuos por un fitness

    Busca todos los individuos de una población que tengan el fitness buscado

    Args:
      population: Población
      target_value: Fitness a buscar

    Returns:
        Diccionario con todos los individuos con el fitness buscado
    """
    return dict(filter(lambda i: i[1] == target_value, population.items()))


def build_initial_population(population_size: int = 100, target_value: int = None):
    """Construye población inicial

    Generamos una población inicial aleatoria. Si el parámetro target_value es pasado, los individuos generados que tengan ese fitness NO serán agregados a la población, para garantizar que el AG generara al menos una generación mas

    Args:
      population_size: Tamaño de la población, por defecto 100
      target_value: Fitness a buscar

    Returns:
      Diccionario con los individuos y su fitness
    """
    population_genes = ""
    individuals = {}
    # Repetir mientras:
    # La población aun no contenga todos los numeros y operadores
    # El tamaño de la población sea menor al que queremos
    while(not population_is_valid(population_genes) or len(individuals) < population_size):
        random_numbers = random.sample(_NUMBERS, 5)
        # No usamos el generador en este caso porque vamos a tomar un numero aleatorio de permutaciones de todo el unvierso posible. Y en cada vuelta repetimos. Como son pocos, no hay impacto
        operations = list(permutations(_OPERATIONS, 4))
        random_operations_length = random.randrange(1, len(operations))
        random.shuffle(operations)
        for j in range(0, random_operations_length):
            # Generamos la expresion
            expression = generate_expresion(random_numbers, operations[j])
            fitness = get_fitness(expression)

            # Si se paso un target_value y el individuo tiene ese fitness, no se guarda. Leer doc arriba
            if (target_value is not None and target_value != fitness) or (target_value is None):
                # Guarda el individuo y su fitness en un diccionario
                individuals[expression] = fitness
                # Saca los genes del individuo y los agrega a los genes unicos de la población para luego verificar que la población tiene todos los numeros y operadores
                population_genes = "".join(set(population_genes + expression))
    return individuals


def order_population_by_fitness(population: dict, reverse_order: bool = True):
    """Ordena los sujetos de la población en base al fitness

    Ordenar la población por el fitness
    El fitness es el valor de la clave en el diccionario
    population.items() nos retorna tuplas por ejemplo ('1+2-3*4/5', 0.6), por eso ordenamos en el indice [1] que es fitness de esa expresion

    Args:
      population: población a ordenar
      reverse_order: Invierte el orden

    Returns:
        población ordenada por fitness
    """
    return dict(sorted(population.items(), key=lambda i: i[1], reverse=reverse_order))


def select_individuals_by_ranking(population: dict):
    """Selección de individuos por fitness

    Seleccionamos en base al fitness del individuo (Ranking), recordando que el fitness de una expresion esta como valor dentro del diccionario. Seleccionamos 1/4 de los mayores y 1/4 de los menores

    Args:
      population: población

    Returns:
        Individuos seleccionados
    """
    population = order_population_by_fitness(population)
    selected_individuals = list(population.items())
    selected_individuals = dict(
        selected_individuals[:_POPULATION_SIZE//4] + selected_individuals[(_POPULATION_SIZE//4)*-1:])
    return selected_individuals


def select_gene_from_random_parents(parents: list, gene_index: int):
    """Selecciona los genes de los padres en una i-esima posición

    Args:
      parents: Lista con los dos padres
      gene_index: Indice del gen que sacaremos de ambos padres

    Returns:
        Tupla con dos valores, el primero es el gen del padre A, y el segundo el gen del padre B
    """
    # Seleccionamos al azar el indice del que sera el padre a. 0-50 para padre a, 51-100 para padre b
    random_parent = 0 if random.randint(0, 100) < 51 else 1
    parent_a = parents[random_parent]
    parent_b = parents[abs(random_parent-1)]
    return parent_a[gene_index], parent_b[gene_index]


def uniform_crossover(parents: list):
    """Cruce uniforme

    Realizamos el cruce de los padres usando uniform crossover. Las expresiones tienen un conjunto de 9 caracteres, serian 9 genes. Como es aleatorio, cada cruce verificamos que la expresion sea una expresion correcta.
    Debido a las restricciones del problema. Vamos a repetir la selección aleatoria del padre, si el gen en la posición i-esima de los padres, ya se encuentra en los hijos. Si reintentamos 20 veces y aun no se consigue un gen candidato, regresamos a los mismos padres

    Args:
      parents: Lista con los dos padres

    Returns:
        Nuevos hijos generados con cruce uniforme
    """
    while True:  # seleccion aleatoria del padre para el gen i
        individual_a = ""
        individual_b = ""
        for gene_index in range(0, 9):
            # Seleccion aleatoria del padre
            retries = 0
            gene_parent_a, gene_parent_b = select_gene_from_random_parents(
                parents, gene_index)
            # Repeticion si los hijos ya tienen el gen elegido
            while gene_parent_a in individual_a or gene_parent_b in individual_b:
                if retries > 20:
                    return parents[0], parents[1]
                gene_parent_a, gene_parent_b = select_gene_from_random_parents(
                    parents, gene_index)
                retries += 1

            # Agregamos el gen al hijo
            individual_a += gene_parent_a
            individual_b += gene_parent_b
        # Retornamos a los hijos solo si sus expresiones son validas
        if expression_is_valid(individual_a) and expression_is_valid(individual_b):
            return individual_a, individual_b
    return None, None


def one_point_crossover(parents: list):
    """Cruce uniforme

    Realizamos el cruce de los padres usando 1-point crossover. Las expresiones tienen un conjunto de 9 caracteres, serian 9 genes. El punto se elige aleatoriamente y se generan los dos hijos de los dos padres

    Args:
      parents: Lista con los dos padres

    Returns:
        Nuevos hijos generados con cruce uniforme
    """
    while True:  # seleccion aleatoria del padre para el gen i
        # Seleccionamos el punto en la secuencia del cromosoma
        random_point = random.randint(0, len(parents[0])-1)

        # Copiamos los genes a los hijos
        individual_a = parents[0][:random_point] + parents[1][random_point:]
        individual_b = parents[1][:random_point] + parents[0][random_point:]

        # Retornamos a los hijos solo si sus expresiones son validas
        if expression_is_valid(individual_a) and expression_is_valid(individual_b):
            return individual_a, individual_b
    return None, None


def mutate_population(population: dict):
    """Mutar un individuo de la población

    Se selecciona un individuo al azar y luego para la mutación seleccionamos dos caracteres al azar de la expresion y los intercambiamos. Este proceso se repetirá hasta que el individuo o expresion generada, sea correcta. Luego el individuo antiguo es eliminado de a población e insertado el nuevo o mutado

    Args:
      population: población

    Returns:
        población con un individuo mutado
    """
    individual, _ = random.choice(list(population.items()))
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

        if expression_is_valid(new_individual):
            population[new_individual] = get_fitness(new_individual)
            return population


def select_random_parents(population: dict):
    """Selecciona padres al azar de una población

    Args:
      population: población de la que se seleccionaran los padres

    Returns:
        Padres seleccionados
    """
    parent_a_expression, _ = random.choice(list(population.items()))
    parent_b_expression, _ = random.choice(list(population.items()))
    return parent_a_expression, parent_b_expression


def generate_children_from_parents(parent_a: str, parent_b: str, target_generation: dict):
    """Genera hijos a partir de dos padres

    Se intenta generar dos hijos a partir de los dos padres. Sin embargo los hijos podrían ya existir en la nueva generación. Por lo tanto se controla generación infinita con una condición, si la cantidad de ciclos supera la (cantidad de genes * 2) se rompe el ciclo y se retornan los mismos padres.

    Abstraemos del algoritmo principal la técnica de cruce, si queremos cambiarla, la cambiamos aquí

    Args:
      parent_a: Padre A
      parent_a: Padre B
      target_generation: generación a la que pertenecerán los hijos

    Returns:
        Hijos generados
    """
    children_a = ""
    children_b = ""
    children_exists = True
    number_of_attempts = 0
    while(children_exists):
        children_a, children_b = uniform_crossover([parent_a, parent_b])
        children_exists = children_a in target_generation.keys(
        ) or children_a in target_generation.keys()
        if number_of_attempts > len(parent_a)*2:
            return parent_a, parent_b
        number_of_attempts += 1
    return children_a, children_b


def genetic_algorithm(initial_population: dict, target_value: int = None):
    """Algoritmo genético

    Si target_value es definido, generara generaciones hasta conseguir un individuo que tenga de fitness el valor buscado. Si target_value no es definido, generara generaciones hasta el máximo permitido

    Args:
      population: población inicial
      target_value: Fitness a buscar

    Returns:
        población final
    """
    global _GENERATIONS_HISTORY
    current_generation = 1
    population = copy.deepcopy(initial_population)

    while(current_generation < _MAX_GENERATIONS):
        # seleccionamos los mejores individuos por ranking
        selected_individuals = select_individuals_by_ranking(population)

        # Nueva generación vacia
        new_generation = {}
        # Ciclo para seleccionar padres al azar y cruzarlos. Los hijos son agregados a la generación nueva
        while(len(new_generation) < _POPULATION_SIZE):
            parent_a_expression, parent_b_expression = select_random_parents(
                selected_individuals)
            children_a, children_b = generate_children_from_parents(
                parent_a_expression, parent_b_expression, new_generation)
            # Agregar individuos a población
            new_generation[children_a] = get_fitness(children_a)
            new_generation[children_b] = get_fitness(children_b)

        # Guardamos la población actual con su score para historia
        _GENERATIONS_HISTORY[str(current_generation)] = {
            "population": list(population.keys()), "score": get_population_score(population)}
        print(
            f'Score población {current_generation}: {_GENERATIONS_HISTORY[str(current_generation)]["score"]}')

        # Mutamos y hacemos la nueva generación la población actual
        population = mutate_population(new_generation)
        current_generation += 1

        # Si estamos buscando un individuo en particual, caso de expresion dado un numero
        # Retornamos una población solo con el individuo encontrado
        if target_value is not None:
            result = find_individuals_by_fitness(population, target_value)
            if len(result.items()):
                return result, True

    return population, False


# Constantes
_GENERATIONS_HISTORY = {}
_POPULATION_SIZE = 100
_MAX_GENERATIONS = 100
# _TARGET_SCORE = 70


def find_max_min_integers_from_random_population():
    """Ejecución AG para conseguir expresiones aleatorias, max, min y enteros """
    global _GENERATIONS_HISTORY
    # población inicial
    population = build_initial_population(_POPULATION_SIZE)
    initial_population = order_population_by_fitness(population)
    start_time = time.time()
    population, _ = genetic_algorithm(population)
    end_time = time.time()

    # Imprimir datos de población inicial para comparar con la final
    print()
    print("*** población inicial ***")
    print(
        f'Score población inicial: {get_population_score(initial_population)}')
    max = list(initial_population)[0]
    min = list(initial_population)[-1]
    print(f'Max = {max} = {initial_population[max]}')
    print(f'Min = {min} = {initial_population[min]}')
    print()

    ###### Generar expresiones aleatorias para hallar max, min y enteros #######
    print()
    print(f'*** poblaciónes generadas ***: {len(_GENERATIONS_HISTORY)}')
    print("Tiempo total: --- %s segundos ---" % (end_time - start_time))
    print(f'Score población final: {get_population_score(population)}')
    population = order_population_by_fitness(population)
    integer_individuals = get_individuals_with_integer_fitness(population)
    max = list(population)[0]
    min = list(population)[-1]
    print(f'Max = {max} = {population[max]}')
    print(f'Min = {min} = {population[min]}')
    print(
        f'cantidad idividuos con fitness entero {len(integer_individuals.items())}. Individuos: ')
    print(integer_individuals.items())
    print()


def find_individual_by_fitness_from_random_initial_population(target_value: int):
    """Ejecución AG para conseguir individuo con fitness especifico """
    global _GENERATIONS_HISTORY
    population = build_initial_population(_POPULATION_SIZE, target_value)
    start_time = time.time()
    population, found = genetic_algorithm(population, target_value)
    end_time = time.time()
    # Imprimir datos en caso de buscar un numero particular
    if found:
        print(
            f'*** poblaciónes generadas hasta encontrar individuo ***: {len(_GENERATIONS_HISTORY)}')
        print("Tiempo total: --- %s segundos ---" % (end_time - start_time))
        print(
            f'Individuos encontrados {len(population.items())}.\nIndividuos:')
        print(population.items())
    else:
        print(f'Individuo no enontrado')
    print()

# endregion


# find_max_min_integers_from_random_population()
# find_individual_by_fitness_from_random_initial_population(15)
