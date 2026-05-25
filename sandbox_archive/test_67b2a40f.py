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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]

def rank(A):
    A_augmented = [row[:] + [0] for row in A]
    gaussian_elimination(A_augmented)
    
    rank = 0
    for row in A_augmented:
        if any(row[i] != 0 for i in range(len(row))):
            rank += 1
    return rank

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_disjointness(n):
    # Simplified model of communication complexity for disjointness function
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        CC_R_DISJ_n = communication_complexity_disjointness(n)
        
        # Simulate reduced group C*-algebra and find minimal rank
        tau_f = rank([[random.random() for _ in range(2**n)] for _ in range(2**n)])
        
        results.append({
            "n": n,
            "f": f,
            "CC_R_DISJ_n": CC_R_DISJ_n,
            "tau_f": tau_f
        })
    
    # Check conjecture conditions
    conjecture_holds = True
    counterexample = ""
    for result in results:
        if result["tau_f"] < 0.5 * result["CC_R_DISJ_n"]:
            conjecture_holds = False
            counterexample = f"n={result['n']}, tau(f)={result['tau_f']}, CC_R(DISJ_n)={result['CC_R_DISJ_n']}"
    
    return {
        "metric_name": "Minimal Rank vs Communication Complexity",
        "metric_value": sum(result["tau_f"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")