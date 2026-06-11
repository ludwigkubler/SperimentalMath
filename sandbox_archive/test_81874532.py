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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quantum_walk(f, n, t):
        state = [1] + [0] * (2**n - 1)
        for _ in range(t):
            new_state = [0] * len(state)
            for i in range(len(state)):
                if state[i] != 0:
                    for j in range(n):
                        if f[i & ((1 << j) - 1)] == (i >> j) & 1:
                            new_state[(i ^ (1 << j)) % len(state)] += state[i]
            state = [x / sum(state) for x in new_state]
        return state
    
    def geometric_entropy(state):
        entropy = 0
        for p in state:
            if p != 0:
                entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        total_entropy = 0
        for t in range(1, 11):
            state = quantum_walk(f, n, t)
            entropy = geometric_entropy(state)
            total_entropy += entropy
        avg_entropy = total_entropy / 10
        results.append(avg_entropy)
    
    if len(results) < 30:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    n = len(results)
    mean = sum(results) / n
    variance = sum((x - mean) ** 2 for x in results) / n
    std_dev = math.sqrt(variance)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": mean <= n ** (1.5 / 2) and std_dev < 0.1 * mean,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "not_enough_support"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")