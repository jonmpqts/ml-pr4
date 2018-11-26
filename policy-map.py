import json
import sys
import math
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

_, input, iteration, output = sys.argv

with open(input, 'r') as f:
    all_results = json.load(f)

actions = {
    '0.0': u'\u2190',
    '1.0': u'\u2193',
    '2.0': u'\u2192',
    '3.0': u'\u2191',
}

results = all_results['gammas']['0.99']
values = results['values'][int(iteration) - 1]
policy = results['policies'][int(iteration) - 1]
policy = [actions[str(action)] for action in policy]
annot = ['{} ({})'.format(p, round(v, 2)) for v, p in zip(values, policy)]
annot = np.array(annot, dtype=object)
values = np.array(values)
length = int(math.sqrt(values.shape[0]))
values = values.reshape((length, length))
annot = annot.reshape((length, length))

sns.set(font_scale=0.9)
sns.heatmap(values, annot=annot, fmt='', cbar=False, xticklabels=False, yticklabels=False)
plt.savefig(output)
