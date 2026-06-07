# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from fractions import Fraction

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Function length must be a power of 2")
    
    min_bits = float('inf')
    for i in range(n):
        bits = [f[j] for j in range(2**n) if (j & (1 << i)) == 0]
        min_bits = min(min_bits, len(set(bits)))
    
    return math.ceil(math.log2(min_bits))

def minimal_quadratic_residue_degree(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Function length must be a power of 2")
    
    residues = set()
    for x in range(1, 2**n):
        y = (x * x) % (2**n)
        residues.add(y)
    
    return len(residues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    V_f_values = []
    D_min_f_squared_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_random_boolean_function(n)
            if communication_complexity_rank(f) > 10:
                continue
            
            V_f = communication_complexity_rank(f)
            D_min_f_squared = minimal_quadratic_residue_degree(f) ** 2
            
            V_f_values.append(V_f)
            D_min_f_squared_values.append(D_min_f_squared)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    V_f_mean = sum(V_f_values) / len(V_f_values)
    D_min_f_squared_mean = sum(D_min_f_squared_values) / len(D_min_f_squared_values)
    correlation_coefficient = (sum((V_f - V_f_mean) * (D_min_f_squared - D_min_f_squared_mean) for V_f, D_min_f_squared in zip(V_f_values, D_min_f_squared_values)) /
                               (len(V_f_values) * math.sqrt(sum((V_f - V_f_mean) ** 2 for V_f in V_f_values)) *
                                math.sqrt(sum((D_min_f_squared - D_min_f_squared_mean) ** 2 for D_min_f_squared in D_min_f_squared_values))))
    
    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient:.4f}"
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": V_f_mean,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    V_f_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(V_f_values)/len(V_f_values):.4f} std={math.sqrt(sum((x - sum(V_f_values)/len(V_f_values))**2 for x in V_f_values))/len(V_f_values):.4f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(V_f_values)/len(V_f_values):.4f} std={math.sqrt(sum((x - sum(V_f_values)/len(V_f_values))**2 for x in V_f_values))/len(V_f_values):.4f} support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")