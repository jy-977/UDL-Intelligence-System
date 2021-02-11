8# qlearningAgents.py
# ------------------
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


from learningAgents import ReinforcementAgent

import random,util


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.values = util.Counter()
        "qvalue 가 저장하는 값"

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if (state,action) not in self.values:
            self.values[(state,action)] = 0.0
        "(state,action)에 해당하는 pair가 기존의 qvalue(self.values)에 없으면 " \
        "values에 새로운pair 추가하고 값은 0.0으로 설정"
        return 0.0
        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
        목적 : Q VALUE를 이용해서 VALUE ( 대표값)을 구함
        legalAction이 없으면 --> 0.0반환
        아니면 legalAction안에있는 action으로 qvalue를 가져와서
        가장 큰 qvalue값을 반환하는 함수

          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"

        #** legal action 뜻--> ?머지"
        legalActions = self.getLegalActions(state) #legal action도 리스트
        if len(legalActions) ==0:
            return 0.0
        tmp = util.Counter()  #util.Counter --> 빈 리스트를 만듦
        for action in legalActions:
            tmp[action]= self.getQvalues(state,action)
        return tmp[tmp.argMax()]
        #tmp.argMax() --> util.py에 있던거였음... 중요한건 적절한 함수를 찾아쓰는것..
        #tmp.argMax() --> tmp 안에 가장큰 action을 찾는것
        #tmp[temp.argMax()]--> 가증큰 action의 qvalue를 찾는것
        #return self.getaction()


    def computeActionFromQValues(self, state):
        """
        목적 : Q VALUE를 이용해서 ACTION을 구함
        위에 함수랑 거의 비슷함
        legalAction이 없으면 --> None 반환
        아니면 legalAction안에있는 action으로 qvalue를 가져와서

          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions()
        if len(legalActions) == 0:
            return None
        tmp = util.Counter()
        for action in legalActions:
            tmp[action] = self.getQvalues(state, action)
        return tmp.argMax()
        #tmp안의 가장 큰 action을 찾는것  // 위에꺼는 qvalue를 찾는거였음


    def getAction(self, state):
        """
        현재 STATE에 대한 ACTION을 받아옴.
        무작위로 랜덤값을 뽑았을때
        1. 앱실론보다 작으면 ACTION (EPSILONE)= RANDOMCHOICE
        2. 앱실론보다 크면 ACTION (1-EPSILONE)= 현재 POLICY를 따르는(LEGAL) ACTION
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if len(legalActions)!=0: #
            if util.flipCoin(self.epsilon):
                action = random.choice(legalActions)
            else :
                action = self.computeActionFromQValues(state)
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
