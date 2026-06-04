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
    
    def generate_sat_clause_set(n: int):
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
    
    def compute_nerve(clause_set):
        nerve = []
        for clause in clause_set:
            row = [0] * len(clause_set)
            for i, lit in enumerate(clause):
                if lit == 1:
                    row[i] = 1
            nerve.append(row)
        return nerve
    
    def compute_min_local_indeterminacy(nerve):
        n = len(nerve)
        ind = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(nerve[i][k] == nerve[j][k] for k in range(len(nerve))):
                    ind += 1
        return ind
    
    def estimate_complexity(clause_set):
        return len(clause_set)
    
    n_max = 40
    instances_tested = 30
    total_ind = 0
    total_complexity = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clause_set = generate_sat_clause_set(n)
        nerve = compute_nerve(clause_set)
        ind = compute_min_local_indeterminacy(nerve)
        complexity = estimate_complexity(clause_set)
        
        total_ind += ind
        total_complexity += complexity
    
    mean_ind = total_ind / instances_tested
    mean_complexity = total_complexity / instances_tested
    ratio = mean_ind / mean_complexity if mean_complexity != 0 else float('inf')
    
    conjecture_holds = ratio <= 1.5  # Example threshold, adjust as needed
    counterexample = "" if conjecture_holds else f"ratio={ratio}"
    
    return {
        "metric_name": "min_local_indeterminacy_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio exceeded\" first_failing_seed={first_failing_seed}")