# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #value iteration : V = max(Q(s,a))를 이용해서 V value를 알아냄
        #결국 이 함수의 목적은 Vvalue를 알아내는것


        for _ in range(self.iterations):
            values = util.Counter()
            #Q(s,a)를 위한 state 받아오기
            for state in self.mdp.getStates()
                #util.Counter 디폴트가 0인 딕셔너리 만들어줌
                 #   Q value를 저장할 딕셔너리 : 키 : action / 값 q value
                QValueForAction = util.Counter()
                
                #Qvalue 계산하기
                for action in self.mdp.getPossibleActions(state):
                    QValueForAction[action] = computeQValueFromValues(state,action)
                
                #argmax 가장 높은 값의 "인덱스"를 반환하기 때문에 다시 배열안에 넣어줘서 값을 value[state]에 넣게 한다.
                value[state] = QValueForAction[QValueForAction.argMax()]
            self.values = value



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #각 state의 Qvalue를 알아냄 
        #Q(s,a) = maxT(s,a,s')[R(s,a,s')+discount*V(s')]

        QValue = 0
        #Transition ==> next state와 probabilty(다음 스테이트에 닿을 확률)
        transitionStatesAndProbs=self.mdp.getTransitionStatesAndProbs(state,action)
        for nextState, prob in transitionStatesAndProbs:
            reward = self.mdp.getReward(state,action,nextState)
            # 값을 다 더해서 qvalue가 됨
            QValue += prob * (reward + self.discount * self.getValue(nextState))
        return QValue


        #V k+1(S)= max sum(prob * (Discount + reward*V k(s') )
        #V k+1(S) 는 Values에 저장되어있고 다음값?
        #V k(s') 는 self.value에 저장됨 현재값

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #qvalue 없이 V value구하는법
        #밑에 getPolicy , get Action, getQvalue 이런거 다 이걸로 불러옴

        #terminal state면 : exit () 암것도 안해도됨
        if self.mdp.isTerminal(state):
            return None
        else: #terminal state 아니면 
            
            actions = self.mdp.getPossibleActions(state)
            max_value = self.getQValue(state, actions[0])
            max_action = actions[0]
            
            for action in actions:
                value = self.getQValue(state, action)
                if max_value <= value:
                    max_value = value
                    max_action = action

            return max_action

            
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
