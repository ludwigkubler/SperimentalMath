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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(-n, n) for _ in range(3)]
        if all(abs(x) != 0 for x in clause):
            cnf.append(clause)
    return cnf

def box_counting_dimension(cnf):
    data = [abs(x) for clause in cnf for x in clause]
    max_size = max(data)
    min_size = 1
    while max_size >= min_size:
        size = (max_size + min_size) / 2
        count = sum(1 for x in data if abs(x) >= size)
        if count > len(data) / 4:
            max_size = size - 0.01
        else:
            min_size = size + 0.01
    return math.log(len(data)) / math.log(max_size)

def resolution_proof_width(cnf):
    # Placeholder for actual DPLL solver implementation
    # For simplicity, we'll use a dummy function that returns a linear value
    return len(cnf) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2*n, 3*n)
    cnf = generate_cnf(n, m)
    
    fractal_dimension = box_counting_dimension(cnf)
    proof_width = resolution_proof_width(cnf)
    
    correlation_coefficient = (fractal_dimension * proof_width) / (max(fractal_dimension, proof_width) ** 2)
    mean_abs_diff = abs(fractal_dimension - proof_width) / max(fractal_dimension, proof_width)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 1
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}, Mean Abs Diff: {mean_abs_diff}"
    
    return {
        "metric_name": "Fractal Dimension vs Resolution Proof Width",
        "metric_value": fractal_dimension,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 2))  # Default to first 30 primes if no seeds provided
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")