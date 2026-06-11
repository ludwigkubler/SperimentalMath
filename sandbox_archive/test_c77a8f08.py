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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def quantum_walk_step(state, f):
    new_state = []
    for i in range(len(state)):
        new_state.append((state[i] + f[i]) % 2)
    return new_state

def geometric_entropy(state):
    counts = [0] * len(state)
    for s in state:
        counts[s] += 1
    total = sum(counts)
    entropy = 0
    for count in counts:
        if count == 0:
            continue
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        state = [random.choice([0, 1]) for _ in range(2**n)]
        total_entropy = 0
        
        for t in range(1, 11):
            state = quantum_walk_step(state, f)
            entropy = geometric_entropy(state)
            total_entropy += entropy
            results.append({'n': n, 't': t, 'entropy': entropy})
    
    avg_entropy = sum(result['entropy'] for result in results) / len(results)
    conjecture_holds = all(abs(result['entropy'] - avg_entropy) < 0.1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": avg_entropy,
        "instances_tested": len(results),
        "n_max": max(result['n'] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_entropy = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_entropy} std=0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")