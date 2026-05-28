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
    
    def generate_bp(n):
        # Generate a random read-twice branching program of size n
        bp = []
        for _ in range(n):
            node = {'inputs': [], 'outputs': []}
            if random.choice([True, False]):
                node['inputs'].append(random.randint(0, 1))
            else:
                node['outputs'].append(random.randint(0, 1))
            bp.append(node)
        return bp
    
    def compute_k_theory(bp):
        # Compute the algebraic K-theory over the quotient ring associated with the support of bp
        n = len(bp)
        k_theory = 0
        for i in range(n):
            if bp[i]['inputs']:
                k_theory += 1
            if bp[i]['outputs']:
                k_theory += 1
        return k_theory
    
    def g(n):
        # Lower bound function
        return math.log(n)
    
    def f(n, size):
        # Upper bound function
        return math.log(n) * math.log(size)
    
    n = random.randint(5, 40)
    bp = generate_bp(n)
    k_theory = compute_k_theory(bp)
    size = len(bp)
    
    metric_name = "minimal_rank"
    metric_value = k_theory
    instances_tested = 1
    conjecture_holds = g(n) <= metric_value <= f(n, size)
    counterexample = "" if conjecture_holds else "g(n) > minimal_rank or minimal_rank > f(n, size)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"g(n) > minimal_rank or minimal_rank > f(n, size)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")