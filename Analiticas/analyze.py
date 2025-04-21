########################################
### Import section
########################################
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from context_data import ContextData, RootContextData, GameContextData, LevelContextData


########################################
### Function section
########################################
def gameSession(eventList):
    """
    Computes the lengths of game sessions based on a list of events.

    This function identifies the start and end of each game session using specific event types 
    ("GAME:START" and "GAME:END") and calculates the duration of each session.

    Args:
        eventList (list): A list of events, where each event contains at least:
            - 'eventType' (str): A string indicating the type of the event (e.g., "GAME:START", "GAME:END").
            - 'timestamp' (int): A numeric value representing the timestamp of the event.

    Returns:
        list: A list with the duration of the extracted game sessions in milliseconds.

    Example:
        >>> events = [
        ...     {"eventType": "GAME:START", "timestamp": 1000},
        ...     {"eventType": "LEVEL:START", "timestamp": 2000},
        ...     {"eventType": "LEVEL:END", "timestamp": 3000},
        ...     {"eventType": "GAME:END", "timestamp": 4000},
        ...     {"eventType": "GAME:START", "timestamp": 5000},
        ...     {"eventType": "GAME:END", "timestamp": 8000},
        ... ]
        >>> gameSessionLengths = gameSession(events)
        >>> print(gameSessionLengths)
        [3000, 3000]
    """
    eventList = sorted(eventList, key=lambda x: x['timestamp'])
    gameSessionLengthMs = []
    for currentEvent in eventList:
        if currentEvent['eventType'] == "GameStart":
            tsSessionStart = currentEvent['timestamp']
        if currentEvent['eventType'] == "GameEnd":
            tsSessionEnd = currentEvent['timestamp']
            gameSessionLengthMs.append(tsSessionEnd-tsSessionStart)
    return gameSessionLengthMs    


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
    #deaths = []
    #levels = []
   # fireActivated=[]
    #hitFire=[]
    #for game in contextStack[-1].games:
        #for level in game.levels:
            #levels.append(dict(levelid=level.id, result = level.levelResult))
            #deaths.extend(level.deaths)
            #fire_activations = sum(1 for e in .events if e.type == "FireActivatedEvent")
            #hit_by_fire=sum(1 for e in game.events if e.type == "TargetHitEvent"and e.Hitter == "Fire")
            #fireActivated.append(fire_activations)
            #hitFire.append(hit_by_fire)
    fireActivated = sum(1 for e in sorted_data if e.get("eventType") == "FireActivatedEvent")
    hitByFire = sum(1 for e in sorted_data if e.get("eventType") == "TargetHitEvent" and e.get("Hitter") == "Fire")
    percentajeFire=hitByFire/fireActivated


    return {
        "gameSessionLengthMs": gameSessionLengthMs,
        "percentajeFire":percentajeFire
        #"deaths": deaths,
        #"levels": levels
    }

def drawHexbinHeatmap(data_list, background_image, output_file, gridsize=(27, 22), extent=[0, 865, 0, 705]):
    """
    Draws a hexbin heatmap over a background image using a list of events containing positions and saves it to a file.

    Args:
        data_list (list): A list of dictionaries containing positions ('x' and 'y' keys) for the heatmap.
        background_image (str): Path to the background image file.
        output_file (str): Path to save the generated heatmap image.
        gridsize (tuple): Number of hexagons in the x and y directions.
        extent (list): The bounding box of the data (x_min, x_max, y_min, y_max).

    Returns:
        None
    """
    # Convert the list of dictionaries to a DataFrame
    data = pd.DataFrame(data_list)

    # Scene dimensions: 27x22 tiles = 864x705px
    fig, ax = plt.subplots(figsize=(27, 22))  # inches

    # Draw the map in the background
    img = plt.imread(background_image)
    ax.imshow(img)

    # Draw a transparent heatmap
    data.plot.hexbin(
        fig=fig,
        ax=ax,
        x="x",
        y="y",
        reduce_C_function=sum,
        gridsize=gridsize,
        extent=extent,
        alpha=0.5,
        cmap='Reds'
    )

    ax.set_xticks(range(0, extent[1], 100))
    ax.set_yticks(range(0, extent[3], 100))
    fig.savefig(output_file)
    print(f"Aggregated heatmap saved as {output_file}")



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
    percentajeFireTotal=0
    all_deaths = []
    all_levels = []

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
            #all_deaths.extend(results["deaths"])
            #all_levels.extend(results["levels"])
            percentajeFireTotal+=results["percentajeFire"]
            print(percentajeFireTotal)
            

            
    # Compute aggregated statistics for game session lengths
    s = pd.Series(all_game_session_lengths)
    print("Aggregated Game Session Length Statistics:")
    print(s.describe())

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