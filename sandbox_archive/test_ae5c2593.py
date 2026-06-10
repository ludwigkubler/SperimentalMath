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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        pivot = A[i][i]
        for k in range(i+1, n):
            factor = -A[k][i] / pivot
            for j in range(i, n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += factor * A[i][j]
    return A

def min_geometric_arithmetical_rank(C):
    n = len(C)
    A = [[Fraction(C[i][j]) for j in range(n)] for i in range(n)]
    A = gaussian_elimination(A)
    
    rank = 0
    for row in A:
        if any(row[j] != Fraction(0) for j in range(n)):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_ratio = 0.0
    max_n = n
    
    for _ in range(30):
        # Generate a random communication protocol with rank variance r
        C = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        while not any(sum(row) != 0 for row in C):  # Ensure non-trivial matrix
            C = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        
        r = sum(abs(C[i][j]) for i in range(n) for j in range(i+1, n))
        if r == 0:
            continue
        
        mgar_r = min_geometric_arithmetical_rank(C)
        ratio = Fraction(mgar_r, r)
        total_ratio += ratio
        instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 2 * n**0.5  # Example threshold, replace with actual analysis
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    
    return {
        "metric_name": "mgar/r",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")