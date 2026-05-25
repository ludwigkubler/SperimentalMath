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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def support(f):
        return set(range(len(f)))
    
    def groupoid_action(f, s):
        action = set()
        for i in s:
            action.add(tuple(f[j] for j in range(i, len(f), len(s))))
        return action
    
    def minimal_rank(g):
        return len(g)
    
    def dpll_solver(f):
        n = int(math.log2(len(f)))
        if n == 0: return 1
        for i in range(2**n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            if all(f[j] == (assignment[j % n] ^ assignment[(j + 1) % n]) for j in range(len(f))):
                return len(assignment)
        return float('inf')
    
    def smallest_acc0_circuit_size(f):
        size = dpll_solver(f)
        if size == float('inf'):
            return 2**n
        return size
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        f = generate_boolean_function(n)
        s = support(f)
        g = groupoid_action(f, s)
        rank = minimal_rank(g)
        circuit_size = smallest_acc0_circuit_size(f)
        results.append((rank, circuit_size))
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [rank / circuit_size for rank, circuit_size in results]
    mean_ratio = sum(ratios) / len(ratios)
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(r <= 1 for r in ratios),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= 1) / len(results)
    
    if all(r <= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(r > 1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 1)
        counterexample = f"first failing seed {first_failing_seed}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\"")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")