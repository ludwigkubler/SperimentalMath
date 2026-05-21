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
    
    def compute_tropical_curve(f):
        n = int(math.log2(len(f)))
        curve = []
        for i in range(n):
            row = []
            for j in range(n):
                if f[2**i + 2**j] == 1:
                    row.append((i, j))
            curve.append(row)
        return curve
    
    def compute_minimal_local_gromov_witten_invariant(curve):
        n = len(curve)
        invariant = 0
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) in curve and (j, i) in curve:
                    invariant += 1
        return invariant
    
    def compute_acc0_circuit_size(f):
        n = int(math.log2(len(f)))
        size = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[2**i + 2**j] == 1:
                    size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        curve = compute_tropical_curve(f)
        invariant = compute_minimal_local_gromov_witten_invariant(curve)
        s_n = compute_acc0_circuit_size(f)
        
        if invariant < math.log(s_n):
            return {
                "metric_name": "min_local_gromov_witten_invariant",
                "metric_value": invariant,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, s(n)={s_n}, invariant={invariant}"
            }
    
    return {
        "metric_name": "min_local_gromov_witten_invariant",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.log(s_n)) / len(results)
    
    if all(r >= math.log(s_n) for r, s_n in zip(results, [compute_acc0_circuit_size(generate_boolean_function(n)) for n in n_values])):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < math.log(s_n) for r, s_n in zip(results, [compute_acc0_circuit_size(generate_boolean_function(n)) for n in n_values])):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, s(n)={s_n}, invariant={min(results)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")