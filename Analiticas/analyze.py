########################################
### Import section
########################################
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from context_data import ContextData, RootContextData, SessionContextData, GameContextData


########################################
### Function section
########################################

def processEventsWithContext(data):
    """
    Procesa eventos usando una pila de context y computa las métricas

    Esta función utiliza un enfoque basado en el contexto para procesar una lista de eventos. 
    Los eventos se procesan secuencialmente y la pila de contexto determina cómo se gestiona cada uno
    
    """
    sorted_data = sorted(data, key=lambda x: x['timestamp'])
    contextStack = []
    currentEventIx = 0
    totalEvents = len(sorted_data)
    contextStack.append(RootContextData(contextStack))

    while currentEventIx < totalEvents:
        currentEvent = sorted_data[currentEventIx]
        if len(contextStack) == 0:
            
            # Si la pila esta vacia para de procesar
            break
        else:
            # Usa el contexto del top de la pila
            currentContext = contextStack[-1]
            # Parsea el evento
            consumeEvent = currentContext.parseEvent(currentEvent)
            # Si se consume el evento, se actualiza el indice
            if consumeEvent:
                currentEventIx += 1

    # Guarda todas las sesiones de juego en una lista
    gameSessionLengthMs = [game.gameSessionLengthMs for game in contextStack[-1].games]

    
    totalNumHitterFire = 0
    totalNumActivateFire = 0
    totalNumHitterSword = 0
    totalNumActivateSword = 0
    triesPuzzle2 = []
    puzzle1Times = []
    puzzle2Times = []

    puzzle1StartEv = 0
    puzzle1EndEv = 0
    puzzle2StartEv = 0
    puzzle2EndEv = 0

    for game in contextStack[-1].games:
        for level in game.levels:
            totalNumHitterFire += level.numHitterFire
            totalNumActivateFire += level.numActivateFire
            totalNumHitterSword += level.numHitterSword
            totalNumActivateSword += level.numActivateSword
            triesPuzzle2.append(level.triesPuzzle2)
            puzzle1Times.append(level.puzzle1Time)
            puzzle2Times.append(level.puzzle2Time)
           
        
            puzzle1StartEv += level.puzzle1StartEv
            puzzle1EndEv += level.puzzle1EndEv
            puzzle2StartEv += level.puzzle2StartEv
            puzzle2EndEv += level.puzzle2EndEv



    return {
        "gameSessionLengthMs": gameSessionLengthMs,
        "totalNumHitterFire": totalNumHitterFire,
        "totalNumActivateFire": totalNumActivateFire,
        "totalNumHitterSword": totalNumHitterSword,
        "totalNumActivateSword": totalNumActivateSword,
        "triesPuzzle2":triesPuzzle2,
        "puzzle1Times":puzzle1Times,
        "puzzle2Times":puzzle2Times,
        "puzzle1StartEv":puzzle1StartEv,
        "puzzle1EndEv":puzzle1EndEv,
        "puzzle2StartEv":puzzle2StartEv,
        "puzzle2EndEv":puzzle2EndEv
    }

########################################
### MAIN section
########################################

if __name__ == '__main__':
    """Main function
    """

    folder_path = './data'
    all_game_session_lengths = []

    
    """Los eventos se transmiten para que se procesen secuencialmente.
       Cada evento se procesa según el context actual (definido por los eventos que ya hemos procesado). 
       Los contexts se apilan para que el evento se procese utilizando el context superior.
       Los eventos pueden activar una operación de extracción en una pila.
    """
    
    all_game_session_lengths = []
    globalHitterFire = 0
    globalActivateFire = 0
    globalHitterSword = 0
    globalActivateSword = 0
    all_triesPuzzle2= []
    puzzle1Times = []
    puzzle2Times = []
    puzzle1Start = 0
    puzzle1End = 0
    puzzle2Start = 0
    puzzle2End = 0

    # Itera sobre los archivos
    for file_name in os.listdir(folder_path):
        # Elimina archivos corruptos
        if file_name.startswith('X'):
            continue
        if file_name.endswith('.json'):  # Procesa JSON
            file_path = os.path.join(folder_path, file_name)

            print(f"Processing file: {file_name}")

            # Abre el json y carga el context
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Procesa eventos
            results = processEventsWithContext(data)

            # Agrega resultados
            all_game_session_lengths.extend(results["gameSessionLengthMs"])
            #Para calculos globales
            globalHitterFire += results["totalNumHitterFire"]
            globalActivateFire += results["totalNumActivateFire"]
            #Para calculos globales
            globalHitterSword += results["totalNumHitterSword"]
            globalActivateSword += results["totalNumActivateSword"]
            all_triesPuzzle2.extend(results["triesPuzzle2"])
            puzzle1Times.extend(results["puzzle1Times"])
            puzzle2Times.extend(results["puzzle2Times"])
            #para porcentaje de abandono
            puzzle1Start += results["puzzle1StartEv"]
            puzzle1End += results["puzzle1EndEv"]
            puzzle2Start += results["puzzle2StartEv"]
            puzzle2End += results["puzzle2EndEv"]

            

            
    # Computa las distintas estadísticas
    s = pd.Series(all_game_session_lengths)
    print("Estadísticas de Longitud de Sesiones de Juego:")
    print(s.describe())


    #calculo abandonos puzle 1
    num_abandonos1 = puzzle1Start - puzzle1End
    print(f"\nAbandonos puzzle 1: {num_abandonos1}")

    if puzzle1Start > 0:
        porcentaje_abandono = (num_abandonos1 / puzzle1Start) * 100
    else:
        porcentaje_abandono = 0

    print(f"Porcentaje de abandono del puzzle 1: {porcentaje_abandono:.2f}%")
    #calculo abandonos puzle 2
    num_abandonos2 = puzzle2Start - puzzle2End
    print(f"\nAbandonos puzzle 2: {num_abandonos2}")
    
    if puzzle2Start > 0:
        porcentaje_abandono = (num_abandonos2 / puzzle2Start) * 100
    else:
        porcentaje_abandono = 0 

    print(f"Porcentaje de abandono del puzzle 2: {porcentaje_abandono:.2f}%")

    
    if globalActivateFire > 0:
        percentageFireGlobal = (globalHitterFire / globalActivateFire) * 100
    else:
        percentageFireGlobal = 0

    print(f"\nPorcentaje global de fuego (Hit/Activated): {percentageFireGlobal}%\n")

    if globalActivateSword > 0:
        percentageSwordGlobal = (globalHitterSword / globalActivateSword) * 100
    else:
        percentageSwordGlobal = 0

    print(f"\nPorcentaje global de golpes del jugador (Hit/Activated): {percentageSwordGlobal}%\n")

    s4 = pd.Series(all_triesPuzzle2)
    print("Lista de intentos del puzzle 2 por partida:"+ str(all_triesPuzzle2))
    print("\nEstadísticas de Intentos del Puzzle 2:")
    print(s4.describe())

    s5 = pd.Series(puzzle1Times)
    print("Lista de tiempos en completar puzzle 1:"+ str(puzzle1Times))
    print("\nEstadísticas de tiempos del puzzle 1:")
    print(s5.describe())

    s6 = pd.Series(puzzle2Times)
    print("Lista de tiempos en completar puzzle 2:"+ str(puzzle2Times))
    print("\nEstadísticas de tiempos del puzzle 2:")
    print(s6.describe())




    