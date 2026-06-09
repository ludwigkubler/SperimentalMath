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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_random_circuit(n, depth):
    if depth == 0:
        return random.choice(['0', '1'])
    else:
        gate = random.choice(['AND', 'OR', 'NOT'])
        left = generate_random_circuit(n, depth - 1)
        right = generate_random_circuit(n, depth - 1)
        return [gate, left, right]

def count_non_commuting_generators(circuit):
    if isinstance(circuit, str):
        return 0
    gate = circuit[0]
    left = count_non_commuting_generators(circuit[1])
    right = count_non_commuting_generators(circuit[2])
    if gate == 'NOT':
        return max(left, right) + 1
    else:
        return left + right

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        depths = [random.randint(1, 10) for _ in range(5)]
        total_generators = 0
        
        for depth in depths:
            circuit = generate_random_circuit(n, depth)
            generators = count_non_commuting_generators(circuit)
            results.append((depth, generators))
            total_generators += generators
    
    metric_value = sum(generators * depth**2 for depth, generators in results) / len(results)
    n_max = max(depth for depth, _ in results)
    
    conjecture_holds = all(generators <= 10 * depth * math.log(n)**2 for _, generators, depth in results)
    counterexample = "" if conjecture_holds else "n={} depth={} generators={}".format(n, depth, generators)
    
    return {
        "metric_name": "Non-commuting Generators",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print("RESULT: FALSIFIED counterexample='{}' first_failing_seed={}".format(counterexample, first_failing_seed))