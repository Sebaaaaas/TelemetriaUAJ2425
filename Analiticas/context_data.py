class ContextData:
    """Abstract class with the main structure of a context data class
    A context data has:
    - A reference to the context stack to push new states
    or pop itself
    - A reference to the parent context, the context that created this.
    It is useful to notify the parent that the child context is removed
    from the context stack

    ContextData contains two important methods:
    - parseEvent: it decides what to do with the current event. This event can
    be consumed (or not)
    - onPopChildContext: what to do when a child context has been removed
    from the context stack
    """

    def __init__(self, contextStack, parentContext = None) -> None:
        """Constructor
        A parent context can be None
        """
        self.contextStack = contextStack
        self.parentContext = parentContext

    def parseEvent(self, event) -> bool:
        """Parses the event.
        Return True if the event must be consumed
        """
        pass

    def popContext(self) -> None:
        """It is the best way to remove itself from the context stack
        because this method notifies the paren context (if exists) that
        the top context has been removed
        """
        childContext = self.contextStack.pop()
        if self.parentContext is not None:
            self.parentContext.onPopChildContext(childContext)        
    
    def onPopChildContext(self,childContextData) -> None:
        """What to do when a child context has been removed from the stack
        
        Keyword arguments:
        childContextData -- The context removed from the stack 
        """
        pass


class RootContextData(ContextData):
    """This is the first context data in the context stack
    It creates game contexts and stores them 
    """

    def __init__(self, contextStack, parentContext=None) -> None:
        """Constructor
        """
        super().__init__(contextStack, parentContext)
        self.games = []
    
    def parseEvent(self, event) -> bool:
        """Creates a new Session context on GAME:START event
        """
        
        if event['eventType'] == "SessionStart":
           self.contextStack.append(SessionContextData(self.contextStack, self))
           # The event is not consumed because it will be used by the game context
           return False
        return True

    def onPopChildContext(self,childContextData) -> None:
        """Stores the session data when removed from the stack
        """
        self.games.append(childContextData)


class SessionContextData(ContextData):
    """Eventos por sesion"""
    """Represents a game session (when the user starts a new game until wins or fails)
    It stores when a game starts and finishes, its length and the information 
    extracted from the levels played during the game session
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
        """It stores information on GAME:START and GAME:END events.
        It also creates a GameContext when a level starts
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
        """Stores a level context when it is removed from the stack
        """
        self.levels.append(childContextData)


class GameContextData(ContextData):

    """It stores information about level events:
    - When the level starts and ends and its lenght
    - The event result
    - Player deaths during this level
    """
    def __init__(self, contextStack, parentContext=None) -> None:
        """Constructor
        """
        super().__init__(contextStack, parentContext)
        self.id = None
        self.tsLevelStart = None
        self.tsLevelEnd = None
        self.levelLengthMs = 0
        self.levelResult = None    
        self.numHitterFire = 0
        self.numActivateFire = 0
        self.triesPuzzle2 = 0
        self.numHitterSword = 0
        self.numActivateSword = 0
        self.puzzle1Start = 0
        self.puzzle1End = 0
        self.puzzle1Time = 0        
        self.puzzle1StartEv = 0
        self.puzzle1EndEv = 0
        self.puzzle2StartEv = 0
        self.puzzle2EndEv = 0

        self.puzzle1Time = None
        self.puzzle2Start = None
        self.puzzle2Time = None        
        

    def parseEvent(self, event) -> bool:
        """Eventos por partida"""
        """It stores data on LEVEL:START and LEVEL:END
        Additionally, it stores death positions in PLAYER:DEATH events
        """
        if event['eventType'] == "GameStart":
            self.id = event["gameID"]
            self.tsLevelStart = event['timestamp']       
        elif (event['eventType'] == "GameEnd"): #and (self.id == event["levelId"]):
           self.tsLevelEnd = event['timestamp'] 
           self.levelLengthMs = self.tsLevelEnd - self.tsLevelStart
          # self.levelResult = event["result"]
           if self.numActivateFire > 0:
                self.percentageFire = (self.numHitterFire / self.numActivateFire) * 100
           else:
                self.percentageFire = 0

           if self.numActivateSword > 0:
                self.percentageSword = (self.numHitterSword / self.numActivateSword) * 100
           else:
                self.percentageSword = 0
            
           self.popContext()

        elif (event['eventType'] == "TargetHitEvent" and event['Hitter']=='Fire'):
            self.numHitterFire+=1
        elif(event['eventType'] == "FireActivatedEvent"):
            self.numActivateFire+=1
        elif (event['eventType'] == "TargetHitEvent" and event['Hitter']=='Sword'):
            self.numHitterSword+=1
        elif(event['eventType'] == "PlayerAttackEvent"):
            self.numActivateSword+=1
        elif(event['eventType']== "Puzzle2ResetEvent" or event['eventType']=='Puzzle2SuccessEvent'):
            self.triesPuzzle2+=1
        elif(event['eventType']== "Puzzle1StartEvent"):
            self.puzzle1Start=event['timestamp']
            self.puzzle1StartEv+=1
        elif(event['eventType']== "Puzzle1EndEvent"):
            self.puzzle1Time=event['timestamp']-self.puzzle1Start
            self.puzzle1End += 1
            self.puzzle1EndEv+=1
        elif(event['eventType']== "Puzzle2StartEvent"):
            self.puzzle2StartEv+=1
            self.puzzle2Start=event['timestamp']
        elif(event['eventType']== "Puzzle2EndEvent"):
            self.puzzle2EndEv+=1
            self.puzzle2Time=event['timestamp']-self.puzzle2Start

    
        return True
