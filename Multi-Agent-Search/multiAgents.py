# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #in this case pacman doesnt move
        if currentGameState.getPacmanPosition() == newPos:
            return -1

        foodList = newFood.asList()
        foodDistance = []
        #for each food compute manhattanDistance between pacman and the food
        for foodPos in foodList:
            foodDistance.append(manhattanDistance(foodPos, newPos))

        ghostPositions = childGameState.getGhostPositions()
        ghostDistance = []
        #for each ghost compute manhattanDistance between pacman and the ghost
        for ghostPos in ghostPositions:
            ghostDistance.append(manhattanDistance(ghostPos, newPos))

        #if ghost is too near to pacman
        if min(ghostDistance) < 2:
            return -1

        #if there is no food left to eat (win)
        if len(foodDistance)==0:
            return float("inf")
        
        totalFoods = len(foodList)
        totalDistanceToAllFoods = sum(foodDistance)

        #we set the numerator of the first fraction as 10000 in order to be greater than 
        #the totalDistanceToAllFoods witch apppears to the denominator
        #we do the same with the other fraction
        #in order to have an evaluation of the state
        return 10000/totalDistanceToAllFoods + 10000/totalFoods

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth):
            #get legal actions for pacman
            actions = gameState.getLegalActions(0)
            #if terminal-test(state) or expanded to the given depth
            if len(actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                #return utility(state)
                return (self.evaluationFunction(gameState), None)

            maxAction = None
            v = -(float("inf"))
            #find the action with the highest value of the minValues
            for action in actions:
                minV = minValue(gameState.getNextState(0,action), 1, depth)
                #save the value
                minV = minV[0]
                if minV > v:
                    v, maxAction = minV, action

            return (v, maxAction)

        def minValue(gameState, ghost, depth):
            #get legal action for ghost 
            actions = gameState.getLegalActions(ghost)
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), None)

            minAction = None
            v = float("inf")  
            #find the action with the lowest value of the maxValues
            for action in actions:
                #if its the last ghost compute the max value
                if ghost == gameState.getNumAgents() - 1:
                    maxV = maxValue(gameState.getNextState(ghost, action), depth + 1)
                else:
                    #compute minValue for the next ghost
                    maxV = minValue(gameState.getNextState(ghost, action), ghost + 1, depth)
                #save the value
                maxV = maxV[0]
                if maxV < v:
                    v, minAction = maxV, action

            return (v, minAction)
                
        #call maxValue for the root
        maxV = maxValue(gameState,0)
        #return the action
        return maxV[1]
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, a, b, depth):
            #get legal actions for pacman
            actions = gameState.getLegalActions(0)
            #if terminal-test(state) or expanded to the given depth
            if len(actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                #return utility(state)
                return (self.evaluationFunction(gameState), None)

            maxAction = None
            v = -(float("inf"))
            #find the action with the highest value of the minValues
            for action in actions:
                minV = minValue(gameState.getNextState(0,action), 1, a, b, depth)
                #save the value
                minV = minV[0]

                if minV > v:
                    v, maxAction = minV, action

                if v > b:
                    return (v, maxAction)
                
                if v > a:
                    a = v

            return (v, maxAction)

        def minValue(gameState, ghost, a, b, depth):
            #get legal action for ghost 
            actions = gameState.getLegalActions(ghost)
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), None)

            minAction = None
            v = float("inf")  
            #find the action with the lowest value of the maxValues
            for action in actions:
                #if its the last ghost compute the max value
                if ghost == gameState.getNumAgents() - 1:
                    maxV = maxValue(gameState.getNextState(ghost, action), a, b, depth + 1)
                else:
                    #compute minValue for the next ghost
                    maxV = minValue(gameState.getNextState(ghost, action), ghost + 1, a, b, depth)
                #save the value
                maxV = maxV[0]

                if maxV < v:
                    v, minAction = maxV, action

                if v<a:
                    return (v, minAction)

                if v<b:
                    b=v

            return (v, minAction)

        #call maxValue for the root
        maxV = maxValue(gameState, -float("inf"), float("inf"), 0)
        #return the action
        return maxV[1]

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, depth):
            #get legal actions for pacman
            actions = gameState.getLegalActions(0)
            #if terminal-test(state) or expanded to the given depth
            if len(actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                #return utility(state)
                return (self.evaluationFunction(gameState), None)

            maxAction = None
            v = -(float("inf"))
            #find the action with the highest value of the minValues
            for action in actions:
                chanceV = chance(gameState.getNextState(0,action), 1, depth)
                #save the value
                chanceV = chanceV[0]

                if chanceV > v:
                    v, maxAction = chanceV, action

            return (v, maxAction)


        def chance(gameState, ghost, depth):
            #get legal action for ghost 
            actions = gameState.getLegalActions(ghost)
            totalActions = len(actions)
            if totalActions == 0:
                return (self.evaluationFunction(gameState), None)

            minAction = None
            v = float("inf")  
            #find the expected value
            sum = 0
            for action in actions:
                #if its the last ghost compute the max value
                if ghost == gameState.getNumAgents() - 1:
                    maxV = maxValue(gameState.getNextState(ghost, action), depth + 1)
                else:
                    #compute expected value for the next ghost
                    maxV = chance(gameState.getNextState(ghost, action), ghost + 1, depth)
                #save the value
                maxV = maxV[0]
                sum += maxV

            #every value has the same propability 1/totalActions
            sum = sum/totalActions
            return (sum, minAction)

        #call maxValue for the root
        maxV = maxValue(gameState, 0)
        #return the action
        return maxV[1]  

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    pacmanPos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    foodList = Food.asList()
    foodDistance = []
    #for each food compute manhattanDistance between pacman and the food
    for foodPos in foodList:
        foodDistance.append(manhattanDistance(foodPos, pacmanPos))

    ghostPositions = currentGameState.getGhostPositions()
    ghostDistance = []
    #for each ghost compute manhattanDistance between pacman and the ghost
    for ghostPos in ghostPositions:
        ghostDistance.append(manhattanDistance(ghostPos, pacmanPos))

    #if ghost is too near to pacman
    if min(ghostDistance) < 3:
        return -100

    totalFoods = len(foodList)
    totalDistanceToAllFoods = sum(foodDistance)
    minFoodDist = min(foodDistance)
    score=scoreEvaluationFunction(currentGameState)
    return  score - (totalDistanceToAllFoods/10 + minFoodDist + 10*totalFoods)

    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
