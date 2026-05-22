# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    def entropy(p):
        return -sum([p[i] * log2(p[i]) for i in range(len(p))])

    def generate_bp(n):
        bp = []
        for _ in range(n):
            bp.append(random.choice(['0', '1']))
        return bp

    def minimal_tensor_product_entropy(bp):
        states = set()
        n = len(bp)
        for i in range(2**n):
            state = ''.join([bp[j] if (i >> j) & 1 else 'X' for j in range(n)])
            states.add(state)
        return entropy([len(states)/2**n])

    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Test each size with 5 different instances
            bp = generate_bp(n)
            ent = minimal_tensor_product_entropy(bp)
            total_entropy += ent
            instances_tested += 1

    mean_entropy = total_entropy / instances_tested
    conjecture_holds = mean_entropy <= n_values[-1] * log2(2)
    counterexample = "" if conjecture_holds else f"Mean entropy {mean_entropy} > {n_values[-1]} * log2(2)"

    return {
        "metric_name": "Minimal Tensor Product Entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")

    mean_entropy = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)

    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Mean entropy exceeds n log(2)\" first_failing_seed={first_failing_seed}")