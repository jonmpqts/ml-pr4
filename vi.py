import sys
import json
import time
import gym
import numpy as np

_, env_name, output = sys.argv


def run_episode(env, policy, gamma):
    obs = env.reset()
    total_reward = 0
    step_idx = 0
    while True:
        obs, reward, done, _ = env.step(int(policy[obs]))
        total_reward += (gamma ** step_idx * reward)
        step_idx += 1
        if done:
            break
    return total_reward, step_idx + 1


def evaluate_policy(env, policy, gamma, n=3):
    episodes = [run_episode(env, policy, gamma) for _ in range(n)]
    return np.mean(episodes, axis=0).tolist()


def extract_policy(env, v, gamma):
    policy = np.zeros(env.nS)
    start = time.clock()
    for s in range(env.nS):
        q_sa = np.zeros(env.action_space.n)
        for a in range(env.action_space.n):
            for next_sr in env.P[s][a]:
                p, s_, r, _ = next_sr
                q_sa[a] += (p * (r + gamma * v[s_]))
        policy[s] = np.argmax(q_sa)
    return policy.tolist(), time.clock() - start


def value_iteration(env):
    v = np.zeros(env.nS)
    max_iterations = 100000
    eps = 1e-20
    iterations = []
    for i in range(max_iterations):
        prev_v = np.copy(v)
        start = time.clock()
        for s in range(env.nS):
            q_sa = [sum([p*(r + prev_v[s_]) for p, s_, r, _ in env.P[s][a]]) for a in range(env.nA)]
            v[s] = max(q_sa)
        iterations.append((v.tolist(), time.clock() - start))
        if np.sum((np.fabs(prev_v - v))) <= eps:
            break
    return iterations


env = gym.make(env_name).unwrapped
values = value_iteration(env)
optimal_policy = extract_policy(env, values[-1][0], 0.99)
optimal_outcome = evaluate_policy(env, optimal_policy[0], 0.99)

gammas = {}

for gamma in [i / 100.0 for i in range(0, 100)]:
    policies = [extract_policy(env, value, gamma) for value, _ in values[0:500]]
    outcomes = [evaluate_policy(env, policy, gamma) for policy, _ in policies]
    gammas[gamma] = {
        'policies': policies,
        'outcomes': outcomes
    }

with open(output, 'w') as f:
    json.dump({
        'values': values,
        'optimal_policy': optimal_policy,
        'optimal_outcome': optimal_outcome,
        'gammas': gammas
    }, f)
