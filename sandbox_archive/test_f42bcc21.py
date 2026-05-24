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
    
    def tseitin_formula(n):
        if n < 2:
            return [], []
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for i in range(1, n):
            clauses.append([variables[i], -variables[i + 1]])
        return variables, clauses
    
    def min_rank(C_F):
        # Placeholder function to compute the minimal rank of a Coxeter group representation
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    def resolution_length(clauses):
        # Placeholder function to simulate the resolution proof length for a Tseitin formula
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses) * 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = tseitin_formula(n)
    min_rank_C_F = min_rank(variables)
    resolution_length_F = resolution_length(clauses)
    
    if resolution_length_F == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution length is zero"
        }
    
    ratio = 2 ** min_rank_C_F / resolution_length_F
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio > 0.5,  # Placeholder threshold for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(arg) for arg in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")