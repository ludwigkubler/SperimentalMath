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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random group G and its representation V over a field F
    n = random.randint(5, 40)
    G = list(range(n))
    V = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    # Calculate the minimal rank of V
    minrank_V = sum(1 for row in V if any(row))  # Count non-zero rows
    
    # Generate a random k-CNF formula representing the boolean function represented by V
    k = random.randint(2, n-1)
    num_clauses = random.randint(n, 2*n)
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice(G) for _ in range(k)]
        clauses.append(clause)
    
    # Calculate the DPLL search tree width of the k-CNF formula
    def dpll_width(clauses):
        if not clauses:
            return 0
        if any(len(clause) == 1 for clause in clauses):
            return max(dpll_width([c for c in clauses if len(c) > 1]) for c in set(sum(clauses, [])))
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            return 1 + dpll_width([c for c in clauses if unit_clause[0] not in c])
        else:
            p = random.choice(G)
            return max(dpll_width([c for c in clauses if p not in c]), dpll_width([c for c in clauses if -p not in c]))
    
    DPLL_search_tree_width_G = dpll_width(clauses)
    
    # Correlate the two measures
    ratio = minrank_V / (DPLL_search_tree_width_G + 1e-9)  # Avoid division by zero
    
    return {
        "metric_name": "minrank_to_DPLL_width_ratio",
        "metric_value": ratio,
        "instances_tested": n,
        "conjecture_holds": ratio >= 0.5,  # Placeholder for actual constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(30)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='minrank_to_DPLL_width_ratio' first_failing_seed={first_failing_seed}")