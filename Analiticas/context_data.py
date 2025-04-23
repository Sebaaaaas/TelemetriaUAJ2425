class ContextData:
    """
       Clase abstracta con la estructura de una clase ContextData
    """

    def __init__(self, contextStack, parentContext = None) -> None:
        """Constructor
        Un contexto "padre" puede ser None
        """
        self.contextStack = contextStack
        self.parentContext = parentContext

    def parseEvent(self, event) -> bool:
        """Parsea los eventos
        Devuelve true si el evento debe ser consumido
        """
        pass

    def popContext(self) -> None:
        """
        Es la mejor manera para eliminarse a si mismo de la pila del context porque notifica al contexto padre (si existe)
        que el contexto top tiene que ser eliminado
        """
        childContext = self.contextStack.pop()
        if self.parentContext is not None:
            self.parentContext.onPopChildContext(childContext)        
    
    def onPopChildContext(self,childContextData) -> None:
        """
           Lo que hace cuando un contexto hijo ha sido eliminado de la pila
        
        Keyword arguments:
        childContextData -- El contexto eliminado de la pila 
        """
        pass


class RootContextData(ContextData):
    """
    Primer context data en la pila de contexto. Crea el contexto de juego y lo guarda
    """

    def __init__(self, contextStack, parentContext=None) -> None:
        """Constructor
        """
        super().__init__(contextStack, parentContext)
        self.games = []
    
    def parseEvent(self, event) -> bool:
        """Crea un nuevo contexto Sesion
        """
        
        if event['eventType'] == "SessionStart":
           self.contextStack.append(SessionContextData(self.contextStack, self))
           # The event is not consumed because it will be used by the game context
           return False
        return True

    def onPopChildContext(self,childContextData) -> None:
        """Guarda la sesión cuando es eliminada de la pila
        """
        self.games.append(childContextData)


class SessionContextData(ContextData):
    """
    Representa una partida
    """
    
    def __init__(self, contextStack, parentContext=None) -> None:
        """Constructor
        """
        super().__init__(contextStack, parentContext)
        self.tsGameStart = None
        self.tsGameEnd = None
        self.gameSessionLengthMs = 0
        self.games = []
        self.levels = [] 

    def parseEvent(self, event) -> bool:
        """
        Guarda informacion de los eventos GameStart y GameEnd y crea un GameContext 
        """
       
        if event['eventType'] == "GameStart":
           # Create a level context and don't consume the event
           self.contextStack.append(GameContextData(self.contextStack, self))
           return False
        elif event['eventType'] == "SessionStart":
           self.tsGameStart = event['timestamp']
        elif (event['eventType'] == "SessionEnd"):
            self.tsGameEnd = event['timestamp'] 
            self.gameSessionLengthMs = self.tsGameEnd - self.tsGameStart
            self.popContext()
        return True
    
    def onPopChildContext(self,childContextData) -> None:
        """Guarda un level context cuando se elimina de la pila

        """
        self.levels.append(childContextData)


class GameContextData(ContextData):

    """
    Guarda la información sobre los eventos del nivel
    """
    def __init__(self, contextStack, parentContext=None) -> None:
        """Constructor
        """
        super().__init__(contextStack, parentContext)
        self.id = None
        self.tsLevelStart = None
        self.tsLevelEnd = None
        self.levelLengthMs = 0    
        self.numHitterFire = 0
        self.numActivateFire = 0
        self.triesPuzzle2 = 0
        self.numHitterSword = 0
        self.numActivateSword = 0
        
        self.puzzle1End = 0       
        self.puzzle1StartEv = 0
        self.puzzle1EndEv = 0
        self.puzzle2StartEv = 0
        self.puzzle2EndEv = 0

        self.puzzleWithPlayer = 0

        self.puzzle1Time = None
        self.puzzle1Start = None
        self.puzzle2Start = None
        self.puzzle2Time = None        
        

    def parseEvent(self, event) -> bool:
        """Eventos por partida"""
        
        #Guarda el tiempo del comienzo de la partida
        if event['eventType'] == "GameStart":
            self.id = event["gameID"]
            self.tsLevelStart = event['timestamp']     
        
        #Guarda el tiempo cuando se ha acabado el nivel y la duracion de la partida, además resta las muertes de los jugadores 
        #para el calculo de la tasa de abandonos
        elif (event['eventType'] == "GameEnd"): 
           if(event['RESULT']== 'FAIL'):
                if(self.puzzleWithPlayer == 1):
                    self.puzzle1StartEv-=1
                elif(self.puzzleWithPlayer == 2):
                    self.puzzle2StartEv-=1
           self.tsLevelEnd = event['timestamp'] 
           self.levelLengthMs = self.tsLevelEnd - self.tsLevelStart
           self.popContext()

        #Número de veces que golpea el fuego en la diana
        elif (event['eventType'] == "TargetHitEvent" and event['Hitter']=='Fire'):
            self.numHitterFire+=1
        #Número de veces que se activa el fuego
        elif(event['eventType'] == "FireActivatedEvent"):
            self.numActivateFire+=1
        #Número de veces que golpea el jugador con la espada en la diana   
        elif (event['eventType'] == "TargetHitEvent" and event['Hitter']=='Sword'):
            self.numHitterSword+=1
        #Número de veces que el jugador pulsa el botón de ataque
        elif(event['eventType'] == "PlayerAttackEvent"):
            self.numActivateSword+=1
        #Número de intentos del puzle 2
        elif(event['eventType']== "Puzzle2ResetEvent" or event['eventType']=='Puzzle2SuccessEvent'):
            self.triesPuzzle2+=1
        #Marca de tiempo al empezar el puzle 1 y las veces que se empieza. También indicador de que el jugador esta en el puzle 1
        elif(event['eventType']== "Puzzle1StartEvent"):
            self.puzzle1Start=event['timestamp']
            self.puzzle1StartEv+=1
            self.puzzleWithPlayer = 1
        #Duración del puzle 1 y ver cuantas veces se acaba (para la tasa de abandonos)
        elif(event['eventType']== "Puzzle1EndEvent"):
            self.puzzle1Time=event['timestamp']-self.puzzle1Start
            self.puzzle1End += 1
            self.puzzle1EndEv+=1
        #Marca de tiempo al empezar el puzle 2 y las veces que se empieza. También indicador de que el jugador esta en el puzle 2
        elif(event['eventType']== "Puzzle2StartEvent"):
            self.puzzle2StartEv+=1
            self.puzzle2Start=event['timestamp']
            self.puzzleWithPlayer = 2
        #Duración del puzle 2 y ver cuantas veces se acaba (para la tasa de abandonos)
        elif(event['eventType']== "Puzzle2EndEvent"):
            self.puzzle2EndEv+=1
            self.puzzle2Time=event['timestamp']-self.puzzle2Start
        
        return True
