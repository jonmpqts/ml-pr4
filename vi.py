import sys
import json
import time
import gym
import numpy as np

_, env_name, gamma, output = sys.argv

env = gym.make(env_name).unwrapped
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
    iterations.append({
        'v': v.tolist(),
        'duration': time.clock() - start
    })
    if (np.sum((np.fabs(prev_v - v))) <= eps):
        print('Value-iteration converged at iteration# %d.' % (i + 1))
        break

with open(output, 'w') as f:
    json.dump(iterations, f)
