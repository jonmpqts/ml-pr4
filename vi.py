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
    """ Evaluates policy by using it to run an episode and finding its
    total reward.
    args:
    env: gym environment.
    policy: the policy to be used.
    gamma: discount factor.
    render: boolean to turn rendering on/off.
    returns:
    total reward: real value of the total reward recieved by agent under policy.
    """
    obs = env.reset()
    total_reward = 0
    max_steps = 100000
    for step_idx in range(max_steps):
        obs, reward, done, _ = env.step(int(policy[obs]))
        total_reward += (gamma ** step_idx * reward)
        step_idx += 1
        if done:
            return total_reward
    return 0.0


def evaluate_policy(env, policy, gamma, n=3):
    """ Evaluates a policy by running it n times.
    returns:
    average total reward
    """
    episodes = [run_episode(env, policy, gamma) for _ in range(n)]
    return np.mean(episodes, axis=0).tolist()


def extract_policy(env, v, gamma):
    """ Extract the policy given a value-function """
    policy = np.zeros(env.nS)
    for s in range(env.nS):
        q_sa = np.zeros(env.action_space.n)
        for a in range(env.action_space.n):
            for next_sr in env.P[s][a]:
                p, s_, r, _ = next_sr
                q_sa[a] += (p * (r + gamma * v[s_]))
        policy[s] = np.argmax(q_sa)
    return policy


def value_iteration(env, gamma):
    """ Value-iteration algorithm """
    policies = []
    changes = []
    values = []
    durations = []
    v = np.zeros(env.nS)
    policy = extract_policy(env, v, gamma)
    max_iterations = 500
    eps = 1e-20
    for i in range(max_iterations):
        prev_v = np.copy(v)
        start = time.clock()
        for s in range(env.nS):
            q_sa = [sum([p*(r + prev_v[s_]) for p, s_, r, _ in env.P[s][a]]) for a in range(env.nA)]
            v[s] = max(q_sa)
        new_policy = extract_policy(env, v, gamma)
        durations.append(time.clock() - start)
        policies.append(new_policy.tolist())
        changes.append(int((new_policy != policy).sum()))
        values.append(v.tolist())
        policy = new_policy

    return {
        'policies': policies,
        'durations': durations,
        'values': values,
        'changes': changes
    }


_, env_name, output = sys.argv
gammas = [0.01, 0.99] + [i / 10.0 for i in range(2, 10, 2)]
env = gym.make(env_name).unwrapped
data = {
    'gammas': {}
}

with Pool(os.cpu_count() - 1) as p:
    results = p.starmap(value_iteration, [(env, gamma) for gamma in gammas])
    for gamma, result in zip(gammas, results):
        #result['rewards'] = p.starmap(evaluate_policy, [(deepcopy(env), policy, gamma) for policy in result['policies']])
        data['gammas'][gamma] = result

with open(output, 'w') as f:
    json.dump(data, f)

sys.exit(0)
#env = gym.make(env_name).unwrapped
#values = value_iteration(env)
#optimal_policy = extract_policy(env, values[-1][0], 0.99)
#optimal_outcome = evaluate_policy(env, optimal_policy[0], 0.99)
#
#gammas = {}
#
#for gamma in [i / 100.0 for i in range(0, 100)]:
#    with Pool(os.cpu_count() - 1) as p:
#        policies = p.starmap(extract_policy, [(env, value, gamma) for value, _ in values[0:500]])
#        outcomes = p.starmap(evaluate_policy, [(gym.make(env_name).unwrapped, policy, gamma) for policy, _ in policies])
##    policies = [extract_policy(env, value, gamma) for value, _ in values[0:500]]
##    outcomes = [evaluate_policy(env, policy, gamma) for policy, _ in policies]
#    gammas[gamma] = {
#        'policies': policies,
#        'outcomes': outcomes
#    }
#
#with open(output, 'w') as f:
#    json.dump({
#        'values': values,
#        'optimal_policy': optimal_policy,
#        'optimal_outcome': optimal_outcome,
#        'gammas': gammas
#    }, f)
