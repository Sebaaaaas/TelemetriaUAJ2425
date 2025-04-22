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
    Processes events using a context stack and computes metrics.

    This function uses a context-based approach to process a list of events. 
    Events are processed sequentially, and the context stack determines how each event is handled. 

    Args:
        data (list): A list of events. Each event is a dictionary containing at least:
            - 'eventType' (str): The type of the event (e.g., "GAME:START", "LEVEL:START").
            - 'timestamp' (int): The timestamp of the event.

    Returns:
        dict: A dictionary containing:
            - "gameSessionLengthMs" (list): A list of game session durations in milliseconds.
            - "deaths" (list): A list of dictionaries representing player deaths, each containing:
                - 'x' (int): The x-coordinate of the death.
                - 'y' (int): The y-coordinate of the death.

    Example:
        >>> sorted_data = [
        ...     {"eventType": "GAME:START", "timestamp": 1000},
        ...     {"eventType": "LEVEL:START", "timestamp": 2000},
        ...     {"eventType": "PLAYER:DEATH", "timestamp": 2500, "x": 10, "y": 20},
        ...     {"eventType": "LEVEL:END", "timestamp": 3000, "levelId": 1, "result": "WIN"},
        ...     {"eventType": "GAME:END", "timestamp": 4000},
        ... ]
        >>> results = process_events_with_context(sorted_data)
        >>> print(results["gameSessionLengthMs"])
        [3000]
        >>> print(results["deaths"])
        [{'x': 10, 'y': 20}]

    Notes:
        - The context stack ensures that events are processed in the correct context.
        - The `RootContextData` object stores all game sessions and their associated metrics.
    """
    sorted_data = sorted(data, key=lambda x: x['timestamp'])
    contextStack = []
    currentEventIx = 0
    totalEvents = len(sorted_data)
    contextStack.append(RootContextData(contextStack))

    while currentEventIx < totalEvents:
        currentEvent = sorted_data[currentEventIx]
        if len(contextStack) == 0:
            
            # If the context stack is empty, stop processing
            break
        else:
            # Use the context at the top of the stack
            currentContext = contextStack[-1]
            # Parse event using the current context
            consumeEvent = currentContext.parseEvent(currentEvent)
            # Some contexts update the stack and leave the event for the next/previous context
            # If the context does not consume the event, we do not increment the index
            if consumeEvent:
                currentEventIx += 1

    # Store all game sessions in a list
    gameSessionLengthMs = [game.gameSessionLengthMs for game in contextStack[-1].games]

    # Store all deaths in a list.
    deaths = []
    levels = []
    totalNumHitterFire = 0
    totalNumActivateFire = 0
    percentageFires = []
    totalNumHitterSword = 0
    totalNumActivateSword = 0
    percentageSword = []
    triesPuzzle2 = []
    puzzle1Times = []

    puzzle1StartEv = 0
    puzzle1EndEv = 0
    puzzle2StartEv = 0
    puzzle2EndEv = 0

   # fireActivated=[]
    #hitFire=[]
    for game in contextStack[-1].games:
        for level in game.levels:
            levels.append(dict(levelid=level.id, result = level.levelResult))
            deaths.extend(level.deaths)
            percentageFires.append(level.percentageFire)
            totalNumHitterFire += level.numHitterFire
            totalNumActivateFire += level.numActivateFire
            percentageSword.append(level.percentageSword)
            totalNumHitterSword += level.numHitterSword
            totalNumActivateSword += level.numActivateSword
            triesPuzzle2.append(level.triesPuzzle2)
            puzzle1Times.append(level.puzzle1Time)
           
        
            puzzle1StartEv += level.puzzle1StartEv
            puzzle1EndEv += level.puzzle1EndEv
            puzzle2StartEv += level.puzzle2StartEv
            puzzle2EndEv += level.puzzle2EndEv

           # fire_activations = sum(1 for e in level.events if e.type == "FireActivatedEvent")
           # hit_by_fire=sum(1 for e in level.events if e.type == "TargetHitEvent"and e.Hitter == "Fire")
           # fireActivated.append(fire_activations)
           # hitFire.append(hit_by_fire)
        #fireActivated = sum(1 for e in sorted_data if e.get("eventType") == "FireActivatedEvent")
        #hitByFire = sum(1 for e in sorted_data if e.get("eventType") == "TargetHitEvent" and e.get("Hitter") == "Fire")
        #percentageFire=hitByFire/fireActivated


    return {
        "gameSessionLengthMs": gameSessionLengthMs,
        #"percentageFire":percentageFire
        "deaths": deaths,
        "levels": levels,
        "percentageFires": percentageFires,
        "totalNumHitterFire": totalNumHitterFire,
        "totalNumActivateFire": totalNumActivateFire,
        "percentagesSword": percentageSword,
        "totalNumHitterSword": totalNumHitterSword,
        "totalNumActivateSword": totalNumActivateSword,
        "triesPuzzle2":triesPuzzle2,
        "puzzle1Times":puzzle1Times,
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

    
    """Approach 2 (Advances): Events are streamed so they are procesed sequentially.
    Every event is processed depending on the current context (defined by the events that
    we have already processed). Contexts are stacked so the event is processed using the top
    context. Events can trigger a pop operation on a stack. 

    In this case, we have a context sessions and levels, and a root context that stores the 
    games (in this example, we don't have sessions). Each context stores metrics and/or other contexts 
    """
    # Initialize lists to aggregate results
    all_game_session_lengths = []
    all_deaths = []
    all_levels = []
    globalHitterFire = 0
    globalActivateFire = 0
    globalHitterSword = 0
    globalActivateSword = 0
    all_triesPuzzle2= []
    puzzle1Times = []
    puzzle1Start = 0
    puzzle1End = 0
    puzzle2Start = 0
    puzzle2End = 0

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        # Remove corrupted files (manually identified, starting with X)
        if file_name.startswith('X'):
            continue
        if file_name.endswith('.json'):  # Process only JSON files
            file_path = os.path.join(folder_path, file_name)

            print(f"Processing file: {file_name}")

            # Open the JSON file and load its contents
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Process events using the context-based approach
            results = processEventsWithContext(data)

            # Aggregate results
            all_game_session_lengths.extend(results["gameSessionLengthMs"])
            all_deaths.extend(results["deaths"])
            all_levels.extend(results["levels"])
            #Lista de porcentajes del fuego por partida
            percentageFiresAll = results["percentageFires"]
            #Para calculos globales
            globalHitterFire += results["totalNumHitterFire"]
            globalActivateFire += results["totalNumActivateFire"]
             #Lista de porcentajes de la espada por partida
            percentageSwordAll = results["percentagesSword"]
            #Para calculos globales
            globalHitterSword += results["totalNumHitterSword"]
            globalActivateSword += results["totalNumActivateSword"]
            all_triesPuzzle2.extend(results["triesPuzzle2"])
            puzzle1Times.extend(results["puzzle1Times"])
            #para porcentaje de abandono
            puzzle1Start = results["puzzle1StartEv"]
            puzzle1End = results["puzzle1EndEv"]
            puzzle2Start = results["puzzle2StartEv"]
            puzzle2End = results["puzzle2EndEv"]

            # print(percentageFireTotal)
            

            
    # Compute aggregated statistics for game session lengths
    s = pd.Series(all_game_session_lengths)
    print("Aggregated Game Session Length Statistics:")
    print(s.describe())


    #calculo abandonos puzle 1
    num_abandonos1 = puzzle1Start - puzzle1End
    print(f"\nAbandonos nivel 1: {num_abandonos1}")

    if puzzle1Start > 0:
        porcentaje_abandono = (num_abandonos1 / puzzle1Start) * 100
    else:
        porcentaje_abandono = 0

    print(f"Porcentaje de abandono del nivel 1: {porcentaje_abandono:.2f}%")
    print(puzzle1Start , puzzle1End)
    #calculo abandonos puzle 2
    num_abandonos2 = puzzle2Start - puzzle2End
    print(f"\nAbandonos nivel 2: {num_abandonos2}")
    
    if puzzle2Start > 0:
        porcentaje_abandono = (num_abandonos2 / puzzle2Start) * 100
    else:
        porcentaje_abandono = 0

    print(f"Porcentaje de abandono del nivel 2: {porcentaje_abandono:.2f}%")
    print(puzzle2Start , puzzle2End)

    s2 = pd.Series(percentageFiresAll)
    print("\nLista de porcentajes de fuego da a la diana con respecto a fuego activado:"+ str(percentageFiresAll))
    if globalActivateFire > 0:
        percentageFireGlobal = (globalHitterFire / globalActivateFire) * 100
    else:
        percentageFireGlobal = 0

    print(f"Porcentaje global de fuego (Hit/Activated): {percentageFireGlobal}%")
    print("\nAggregated Fire Percentage Statistics:")
    print(s2.describe())

    s3 = pd.Series(percentageSwordAll)
    print("Lista de porcentajes de golpes que da el jugador a la diana con respecto al número de golpes totales:"+ str(percentageSwordAll))
    if globalActivateSword > 0:
        percentageSwordGlobal = (globalHitterSword / globalActivateSword) * 100
    else:
        percentageSwordGlobal = 0

    print(f"Porcentaje global de golpes del jugador (Hit/Activated): {percentageSwordGlobal}%")
    print("\nAggregated Sword Percentage Statistics:")
    print(s3.describe())

    s4 = pd.Series(all_triesPuzzle2)
    print("Lista de intentos del puzzle 2 por partida:"+ str(all_triesPuzzle2))
    print("\nAggregated Tries Puzzle 2 Statistics:")
    print(s4.describe())

    s5 = pd.Series(puzzle1Times)
    print("Lista de tiempos en completar puzle 1:"+ str(puzzle1Times))
    print("\nAggregated Times Puzzle 1 Statistics:")
    print(s5.describe())


    # # Create a DataFrame for all deaths and generate a heatmap
    # dfDeaths = pd.DataFrame(all_deaths)

    # # Scene dimensions: 27x22 tiles = 864x705px
    # fig, ax = plt.subplots(figsize=(27, 22))  # inches

    # # We draw the map in the background
    # img = plt.imread("bg.png")
    # ax.imshow(img)
    # # Then, we draw a transparent heatmap 
    # drawHexbinHeatmap(
    #     data_list=all_deaths,
    #     background_image="bg.png",
    #     output_file="aggregated_heatmap.png"
    # )