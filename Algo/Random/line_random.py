import math
import random
import itertools
import matplotlib.pyplot as plt
from tqdm import tqdm

import numpy as np
import numba
import numpy.random
from collections import deque

import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Embedding, Reshape
from tensorflow.keras.optimizers import Adam
from Env.Line_World.line_world import LineWorld

def initP(env):
    P = {}
    for state in env.states:
        st = env.current_state
        for action in env.actions:
            env.current_state = state
            env.step(action)
            state_ = env.current_state
            reward_= env.reward
            done_ = env.done
            stt = env.current_state
            P[(stt, reward_, st, action)] = 1
    return P

def evaluate_policy(env, V, policy, discount_factor=0.9):
    theta=1e-6
    P = initP(env)
    #Initialize the Value function 
    #V = np.zeros((world.grid_size[0],world.grid_size[1]))
    
    while True:
        DELTA = 0
        for s in env.states:
            m_state = env.current_state
            old_V = V[m_state]
            weight = 1 / len(policy[m_state])
            for action in policy[m_state]:
                total = 0
                for key in P:
                    (newState, reward, oldState, act) = key
                    if oldState == m_state and act == action:
                        total += weight*P[key]*(reward+discount_factor*V[newState])
            V[m_state] = total
            DELTA = max(DELTA, np.abs(old_V-V[m_state]))
            
        if DELTA < theta:
            return V            

        
def policy_improvement(env, V, policy, discount_factor=0.9):
    policy_stable = True
    newPolicy = {}
    for s in env.states:
        m_state = env.current_state
        old_actions = policy[m_state]
        value = []
        newAction = []
        P = initP(env)
        for action in old_actions:
            total = 0
            weight = 1 / len(policy[m_state])
            for key in P:
                (newState, reward, oldState, act) = key
                if oldState == m_state and act == action:
                    total += weight*P[key]*(reward+discount_factor*V[newState])
                    value.append(np.round(total, 2))
                    newAction.append(action)  
                    
        value = np.array(value) #Get the list of gotten value actions in the current state
        print(value)
        best = np.where(value == value.max())[0] #Get the position of the best gotten value action
        bestActions = [newAction[item] for item in best]
        newPolicy[m_state] = bestActions
        
        if old_actions != bestActions:
            policy_stable = False
    return policy_stable, newPolicy

def policy_iteration(env, discount_factor=0.9):
    
    #Initialize the policy
    V = np.random.random((len(env.states),))
    policy = {}
    for state in env.states:
        # equiprobable random strategy
        policy[state] = env.actions
    print("Policy : ")
    print(policy)
    V = evaluate_policy(env, V, policy, discount_factor=0.9)
    print("V = ")
    print(V)
    
    policy_stable = False
    while not policy_stable:
        old_policy = policy.copy()
        
        print("Start of policy evaluation")
        #Evaluate the policy
        V = evaluate_policy(env, V, policy, discount_factor=0.9)
        print("V = ")
        print(V)
        
        print("Start of policy Improvement")
        #Improve the policy
        policy_stable, policy =  policy_improvement(env, V, policy, discount_factor=0.9)
        print("Policy : ")
        print(policy)
    
        """if all(old_policy[s] == policy[s] for s in grid.stateSpace.values()):
            break"""
            
    return policy
 
if __name__ == '__main__':
    # Il faut choisir un nombre entre 0 et 3
    # Si l'action est 0, déplacement vers le haut
    # Si l'action est 1, déplacement vers le bas
    # Si l'action est 2, déplacement vers la gauche
    # Si l'action est 3, déplacement vers la droite
    world = LineWorld() #taille, position de départ, fin de jeu reward positive, fin de jeu reward négative
    policy_iteration(world, discount_factor=0.9)
    

