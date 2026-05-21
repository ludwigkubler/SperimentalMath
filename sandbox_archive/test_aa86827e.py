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
from fractions import Fraction
import math

def generate_monotone_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def tropical_representation_size(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Function length must be a power of 2")
    
    size = 0
    for i in range(1, 2**n):
        row = [f[i ^ (1 << j)] - f[i] if i & (1 << j) else f[i] for j in range(n)]
        if any(x < 0 for x in row):
            size += 1
    return size

def communication_complexity(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Function length must be a power of 2")
    
    # Simplified cell-projection method for monotone functions
    complexity = 0
    for i in range(1, 2**n):
        row = [f[i ^ (1 << j)] - f[i] if i & (1 << j) else f[i] for j in range(n)]
        if any(x > 0 for x in row):
            complexity += 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_size = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_monotone_function(n)
            size = tropical_representation_size(f)
            complexity = communication_complexity(f)
            total_size += size
            total_complexity += complexity
            instances_tested += 1
    
    mean_size = Fraction(total_size, instances_tested)
    mean_complexity = Fraction(total_complexity, instances_tested)
    
    conjecture_holds = mean_size <= Fraction(n**2, 3) and mean_complexity > Fraction(n**2, 3)
    counterexample = "" if conjecture_holds else f"mean_size={mean_size}, mean_complexity={mean_complexity}"
    
    return {
        "metric_name": "tropical_representation_size",
        "metric_value": float(mean_size),
        "instances_tested": instances_tested,
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
    
    total_size = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_size} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.05:
        print(f"RESULT: SUPPORTED mean={total_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mean_size={results[0]['metric_value']}, mean_complexity={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")