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
    """ Runs an episode and return the total reward """
    obs = env.reset()
    total_reward = 0
    max_steps = 100000
    for step_idx in range(max_steps):
        obs, reward, done, _ = env.step(policy[obs])
        total_reward += (gamma ** step_idx * reward)
        if done:
            return total_reward
    return 0.0


def evaluate_policy(env, policy, gamma, n=3):
    scores = [run_episode(env, policy, gamma) for _ in range(n)]
    return np.mean(scores)


def extract_policy(v, gamma):
    """ Extract the policy given a value-function """
    policy = np.zeros(env.nS)
    for s in range(env.nS):
        q_sa = np.zeros(env.nA)
        for a in range(env.nA):
            q_sa[a] = sum([p * (r + gamma * v[s_]) for p, s_, r, _ in  env.P[s][a]])
        policy[s] = np.argmax(q_sa)
    return policy


def compute_policy_v(env, policy, gamma):
    """ Iteratively evaluate the value-function under policy.
    Alternatively, we could formulate a set of linear equations in iterms of v[s]
    and solve them to find the value function.
    """
    v = np.zeros(env.nS)
    eps = 1e-10
    while True:
        prev_v = np.copy(v)
        for s in range(env.nS):
            policy_a = policy[s]
            v[s] = sum([p * (r + gamma * prev_v[s_]) for p, s_, r, _ in env.P[s][policy_a]])
        if (np.sum((np.fabs(prev_v - v))) <= eps):
            # value converged
            break
    return v


def policy_iteration(env, gamma):
    """ Policy-Iteration algorithm """
    policies = []
    changes = []
    values = []
    durations = []
    policy = np.random.choice(env.nA, size=(env.nS))  # initialize a random policy
    max_iterations = 500
    for i in range(max_iterations):
        start = time.clock()
        old_policy_v = compute_policy_v(env, policy, gamma)
        new_policy = extract_policy(old_policy_v, gamma)
        durations.append(time.clock() - start)
        policies.append(new_policy.tolist())
        changes.append(int((new_policy != policy).sum()))
        values.append(old_policy_v.tolist())
        policy = new_policy

    return {
        'policies': policies,
        'durations': durations,
        'values': values,
        'changes': changes,
    }


_, env_name, output = sys.argv
gammas = [0.01, 0.99] + [i / 10.0 for i in range(2, 10, 2)]
env = gym.make(env_name).unwrapped
data = {
    'gammas': {}
}

with Pool(os.cpu_count() - 1) as p:
    results = p.starmap(policy_iteration, [(env, gamma) for gamma in gammas])
    for gamma, result in zip(gammas, results):
        #result['rewards'] = p.starmap(evaluate_policy, [(deepcopy(env), policy, gamma) for policy in result['policies']])
        data['gammas'][gamma] = result

with open(output, 'w') as f:
    json.dump(data, f)
