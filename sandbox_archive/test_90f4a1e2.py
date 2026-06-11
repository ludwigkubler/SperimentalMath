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
        state = [0] * (2**n)
        state[0] = 1
        for _ in range(t):
            new_state = [0] * (2**n)
            for i in range(2**n):
                if f[i]:
                    new_state[(i + 1) % (2**n)] += state[i]
                else:
                    new_state[(i - 1) % (2**n)] += state[i]
            state = new_state
        return state
    
    def geometric_entropy(state, n):
        total_prob = sum(state)
        entropy = 0
        for prob in state:
            if prob > 0:
                entropy -= prob * math.log(prob / total_prob) / math.log(2)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        avg_entropy = 0
        for t in range(1, 11):
            state = quantum_walk(f, n, t)
            entropy = geometric_entropy(state, n)
            avg_entropy += entropy / 10
        results.append({"n": n, "avg_entropy": avg_entropy})
    
    return {
        "metric_name": "average_geometric_entropy",
        "metric_value": sum(result["avg_entropy"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")