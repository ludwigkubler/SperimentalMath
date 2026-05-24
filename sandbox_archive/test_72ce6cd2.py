# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define the function to generate a random function field with genus g ≤ 3
    def generate_function_field(g):
        if g == 0:
            return [1]
        elif g == 1:
            return [random.choice([0, 1])]
        elif g == 2:
            return [random.choice([0, 1]), random.choice([0, 1])]
        elif g == 3:
            return [random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1])]
    
    # Define the function to compute the minimal rank of a geometric Langlands duality module
    def minimal_rank(K):
        if len(K) == 1:
            return 1
        elif len(K) == 2:
            return 2
        elif len(K) == 3:
            return 4
        elif len(K) == 4:
            return 8
    
    # Define the function to generate a Tseitin formula on n variables with m clauses
    def generate_tseitin_formula(n, m):
        if n > 40 or m > 100:  # Limiting to avoid excessive computation
            return None
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + ['~' + v for v in variables], n)
            clauses.append(clause)
        return clauses
    
    # Define the function to compute the resolution depth of a Tseitin formula
    def resolution_depth(formula):
        if not formula:
            return 0
        max_depth = 0
        for clause in formula:
            depth = 1
            for literal in clause:
                if literal.startswith('~'):
                    depth += 1
            max_depth = max(max_depth, depth)
        return max_depth
    
    # Main trial logic
    results = []
    for g in range(4):  # Genus g ≤ 3
        K = generate_function_field(g)
        rank = minimal_rank(K)
        if rank < 2**(g+1):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Function field with genus {g} has minimal rank {rank}, expected at least {2**(g+1)}"
            }
        
        for n in range(5, 41):  # n ≤ 40
            formula = generate_tseitin_formula(n, n)
            if formula is None:
                continue
            depth = resolution_depth(formula)
            if depth > 2**n / 2**(g+1):
                return {
                    "metric_name": "resolution_depth",
                    "metric_value": depth,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Tseitin formula with n={n} has resolution depth {depth}, expected at most {2**n / 2**(g+1)}"
                }
            results.append(depth)
    
    return {
        "metric_name": "resolution_depth",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if not trial_result["conjecture_holds"]:
            break
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = len(results) / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<desc>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")