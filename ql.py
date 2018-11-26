# https://medium.com/@m.alzantot/deep-reinforcement-learning-demysitifed-episode-2-policy-iteration-value-iteration-and-q-978f9e89ddaa

import sys
import json
import time
import os
from copy import deepcopy
from multiprocessing import Pool
import gym
import numpy as np


def run_episode(env, policy, gamma):
    obs = env.reset()
    total_reward = 0
    step_idx = 0
    for _ in range(t_max):
        a, b = obs_to_state(env, obs)
        action = policy[a][b]
        obs, reward, done, _ = env.step(action)
        total_reward += (gamma ** step_idx * reward)
        step_idx += 1
        if done:
            break
    return total_reward


def obs_to_state(env, obs):
    """ Maps an observation to state """
    env_low = env.observation_space.low
    env_high = env.observation_space.high
    env_dx = (env_high - env_low) / env.nS
    a = int((obs[0] - env_low[0]) / env_dx[0])
    b = int((obs[1] - env_low[1]) / env_dx[1])
    return a, b


def choose_action(state, epsilon):
    action = 0
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state, :])
    return action


def learn(state, state2, reward, action):
    predict = Q[state, action]
    target = reward + gamma * np.max(Q[state2, :])
    Q[state, action] = Q[state, action] + lr_rate * (target - predict)


def q_learning(env, gamma, min_lr, initial_lr, t_max):
    Q = np.zeros((env.observation_space.n, env.observation_space.n))
    return

    s = env.reset()
    policies = []
    durations = []
    Q = np.zeros([env.observation_space.n, env.action_space.n])
    max_iterations = 2000

    for i in range(max_iterations):
        s = env.reset()
        rAll = 0
        j = 0
        while j < 99:
            j += 1
            a = np.argmax(Q[s,:] + np.random.randn(1, env.action_space.n) * (1. / (i + 1)))
            s1, r, d, _ = env.step(a)
            Q[s,a] = Q[s,a] + 0.7 * (r + gamma * np.max(Q[s1,:]) - Q[s,a])
            rAll += r
            s = s1
            if d:
                break

    print(Q)
    return


    q_table = np.zeros((env.unwrapped.nS, env.unwrapped.nS, 3))
    policy = np.argmax(q_table, axis=2)
    eps = 0.02
    max_iterations = 1000
    for i in range(max_iterations):
        start = time.clock()
        obs = env.reset()
        total_reward = 0
        eta = max(min_lr, initial_lr * (0.85 ** (i // 100)))
        for j in range(t_max):
            a, b = obs_to_state(env, obs)
            if np.random.uniform(0, 1) < eps:
                action = np.random.choice(env.action_space.n)
            else:
                logits = q_table[a][b]
                logits_exp = np.exp(logits)
                probs = logits_exp / np.sum(logits_exp)
                action = np.random.choice(env.action_space.n, p=probs)
            obs, reward, done, _ = env.step(action)
            total_reward += reward
            a_, b_ = obs_to_state(env, obs)
            q_table[a][b][action] = q_table[a][b][action] + eta * (reward + gamma * np.max(q_table[a_][b_]) - q_table[a][b][action])
            if done:
                break
        durations.append(time.clock() - start)
        new_policy = np.argmax(q_table, axis=2)
    return policies



_, env_name, output = sys.argv
gamma = 0.99
epsilon = 0.9
lr_rate = 0.81
env = gym.make(env_name)
policies = q_learning(env, gamma, min_lr, initial_lr, t_max)
#print(policies[-1])
