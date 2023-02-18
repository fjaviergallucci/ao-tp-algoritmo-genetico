from more_itertools import locate
import copy

# #Reglas
# - Los actores del doblaje deben coincidir en las tomas en las que sus personajes aparecen juntos en las diferentes tomas.
# - Los actores de doblaje cobran todos la misma cantidad por cada día que deben desplazarse hasta el estudio de grabación independientemente del número de tomas que se graben
# - No es posible grabar más de 6 tomas por día
# - El objetivo es planificar las sesiones por día de manera que el gasto por los servicios de los actores de doblaje sea el menor posible

_TAKES = [
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
]
_TAKES_PER_DAY = 6

sesiones = []


def get_takes_by_actor():
    takes_by_actor = [{"actor": -1, "takes": []} for _ in _TAKES[0]]
    for i, take in enumerate(_TAKES):
        # Sacar los indices de los actores que participan en la toma
        actors = list(locate(take, lambda x: x == 1))
        for actor in actors:
            takes_by_actor[actor]["actor"] = actor
            takes_by_actor[actor]["takes"].append(i)
        print(actors)
    takes_by_actor = sorted(
        takes_by_actor, key=lambda actor: len(actor["takes"]), reverse=True)
    print(takes_by_actor)

def build_sessions():
    sessions = []
    day_session = {
        "actor" : -1,
        "take" : -1
    }
    takes_by_actor = get_takes_by_actor()
    for actor in takes_by_actor:
        actor_takes = copy.deepcopy(actor["takes"])
        takes = 0
        current_session = 0
        sessions[current_session] = []
        # while( len(sessions[current_session]) < 6):
        for actor_take in actor_takes:
            sessions[current_session] = []
            

        # while(len(actor_takes)):


    
