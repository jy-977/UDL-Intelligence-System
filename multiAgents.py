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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
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

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """
        evatation에 영향을 주는 요소 3가지 : 음식, ghost, capsuel(fruit)
        """

        total_score = 0.0
        oldFood = currentGameState.getFood()
        for x in xrange(oldFood.width):
            for y in xrange(oldFood.height):
                if oldFood[x][y]: #boolean으로 위치에 음식이 있는지 확인
                    d = manhattanDistance((x,y),newPos) #pacman의 새로운 위치로부터 거리를 츠겅
                    if d==0:    #음식 먹었을떄
                        total_score += 100    
                    else:       #음식 멀떄
                        total_score += 1.0/(d*d)
        #여기까지하면 ghost 상관안하고 음식에 가까워지려고함



        #여기서 부터 ghost를 신경쓰기 시작함
        for ghost in newGhostStates:
            d = manhattanDistance(ghost.getPosition(),newPos) #pacman -ghost거리 계산
            if d<=1:      #1만큼 가까워졌을때
                if (ghost.scaredTimer!=0) : #fruit먹은상태면 ghost를 먹을수 있으니까 점수많이줌
                    total_score += 2000
                else :    #아니면 안좋은거니까 점수 깎음
                    total_score -= 200
        
        #capsule : fruit 
        for capsule in currentGameState.getCapsules():
            d = manhattanDistance(capsule, newPos)
            if d==0:
                total_score += 100
            else:
                total_score +=1.0/(d)


        return total_score
        #util.raiseNotDefined()
        #return successorGameState.getScore()

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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        """
        트리의 말단 (leaf)에서 각각의 값을 알아야 min/max를 위한 계산을 할수 있다 --> evaluation function을 호출함
        """
        import sys
        
        def result(gameState,agent,action):  #다음 (successor) state(위치)를 반환함
          return gameState.generateSuccessor(agent,action)
        
        def utility(gameState): #점수 반환 - leaf를 알기위해서
          return self.evaluationFunction(gameState)
        
        #몇개의 depth가남았는지 / depth 가 0 이면 이겼는지 졌는지 반환
        def terminalTest(gameState, depth):  #depth 는 얼마나 더 들어갈수 있는지 그러니까 leaf가 0 
          return depth==0 or gameState.isWin() or gameState.isLose()

        def max_value(gameState, agent, depth):
          #마지막단(terminal test)이면 점수반환(utility) 
          if terminalTest(gameState,depth): return utility(gameState)
          #초기화
          v = -sys.maxint
          #가능한 statate (getLegalActions)를 다 순환한다
          for a in gameState.getLegalActions(agent):
            #min value중에서 가장 큰거 고름
            #다음 state들 (result(,,,))의 값을 받아옴 (minvalue)
            v = max(v,min_value(result(gameState,agent,a),1,depth))
          return v

        def min_value(gameState, agent, depth):
          if terminalTest(gameState,depth): return utility(gameState)
          v = sys.maxint
          for a in gameState.getLegalActions(agent):
            #agent가 2개인 상황일때 인가..? 몇개인지는 모르겠지만 agent가 여려개인 상황일떄
            if (agent == gameState.getNumAgents()-1):   #0번쨰 agnet
              v = min(v, max_value(result(gameState,agent,a),0,depth-1))
            else:                                       #1번째 agent
              v = min(v, min_value(result(gameState,agent,a),agent+1,depth))
          return v

        #초기화 왜 -로? : 
        v = -sys.maxint
        actions=[]
        #getLegalActions(0- pacman) :팩맨위치 받아옴
        for a in gameState.getLegalActions(0):
           #1 첫번째ghost에 대해서만 처리해줌 ==> 나머지 ghost들은 min_value안에서 처리
          #기본적으로 구조가 min (agent 1)> min(agent 2)> max순 (max가제일낮음)
          u = min_value(result(gameState,0,a),1,self.depth)
          #u==v :현재까지 나온 값중에서 좋은 값이니까 ==> 저장
          if u==v: actions.append(a)
         #u>=v 는 처음에 v 가 -sys.maxint일떄 v를 u로 초기화해주고 action 을 a로 설정
          
          elif u>=v :
            v = u
            actions=[a]

        return random.choice(actions)


   #    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        import sys
        def result(gameState,agent,action):
          return gameState.generateSuccessor(agent,action)
        
        def utility(gameState):
          return self.evaluationFunction(gameState)
        
        def terminalTest(gameState, depth):
          return depth==0 or gameState.isWin() or gameState.isLose()

        def max_value(gameState, agent, depth, alpha, beta):
          if terminalTest(gameState,depth): return utility(gameState)
          v = -sys.maxint
          for a in gameState.getLegalActions(agent):
            v = max(v,min_value(result(gameState,agent,a),1,depth, alpha, beta))
            if v > beta : return v
            alpha = max(alpha, v)
          return v

        def min_value(gameState, agent, depth, alpha, beta):
          if terminalTest(gameState,depth): return utility(gameState) 
          v = sys.maxint
          for a in gameState.getLegalActions(agent):
            if (agent == gameState.getNumAgents()-1):
              v = min(v, max_value(result(gameState,agent,a),0,depth-1, alpha, beta))
            else:
              v = min(v, min_value(result(gameState,agent,a),agent+1,depth, alpha, beta))
            if v < alpha : return v
            beta = min(beta,v)
          return v

        v = -sys.maxint
        actions=[]

        #alph - maximum : 초기화는 -infinite
        alpha= -sys.maxint
        #beta - minimum : 초기화는 +infinite
        beta = sys.maxint
        
        for a in gameState.getLegalActions(0):
          u = min_value(result(gameState,0,a),1,self.depth, alpha, beta)
          if u==v: actions.append(a)
          elif u>=v :
            v = u
            actions=[a]
          #여기서 alpha update해주는 이유 :다른 가지 pruning 해주려고  
          alpha = max(alpha,v)

        return random.choice(actions)
  
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
      min value 에서 :  leave들의 평균값으로 
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        import sys
        def result(gameState,agent,action):
          return gameState.generateSuccessor(agent,action)
        
        def utility(gameState):
          return self.evaluationFunction(gameState)
        
        def terminalTest(gameState, depth):
          return depth==0 or gameState.isWin() or gameState.isLose()

        #고친거 없음
        def max_value(gameState, agent, depth):
          if terminalTest(gameState,depth): return utility(gameState)
          v = -sys.maxint
          for a in gameState.getLegalActions(agent):
            v = max(v,min_value(result(gameState,agent,a),1,depth))
          return v

        #min밑에 있는 value들의 평균값만 계산해줌
        def min_value(gameState, agent, depth):
          if terminalTest(gameState,depth): return utility(gameState)
          #평균값만 계산해주는거니까 v에 값들 다 모아놔서 나중에 계산
          #따라서 v는 특정값으로 초기화 안하고 , 그냥 값 담아두는 공간으로만 쓴다
          v= []
          for a in gameState.getLegalActions(agent):
            if (agent == gameState.getNumAgents()-1):
              #그냥 값 다 v에 때려넣음
              v.append(max_value(result(gameState,agent,a),0,depth-1))
            else:
              #그냥 값 다 v에 때려넣음
              v.append(min_value(result(gameState,agent,a),agent+1,depth))
          #평균값 계산
          return sum(v)/float(len(v))

       
        v = -sys.maxint
        actions=[]
        
        for a in gameState.getLegalActions(0):
         
          u = min_value(result(gameState,0,a),1,self.depth)
          
          if u==v: actions.append(a)
          elif u>=v :
            v = u
            actions=[a]

        return random.choice(actions)


        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

