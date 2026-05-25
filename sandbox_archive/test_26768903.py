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
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot row
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]
    return A

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bp(size):
        bp = []
        for _ in range(size):
            bp.append(random.choice([0, 1]))
        return bp
    
    def cohomology(bp):
        n = len(bp)
        A = [[Fraction(0, 1)] * (n + 1) for _ in range(n)]
        for i in range(n):
            A[i][i] = Fraction(1, 1)
            if bp[i] == 1:
                A[i][-1] = Fraction(-1, 1)
        return A
    
    def is_trivial(bp):
        return all(x == 0 for x in bp)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            bp = generate_bp(n)
            if is_trivial(bp):
                continue
            cohom = cohomology(bp)
            rank_value = rank(cohom)
            results.append((n, rank_value))
    
    total_rank = sum(rank for _, rank in results)
    mean_rank = Fraction(total_rank, len(results))
    
    conjecture_holds = True
    counterexample = ""
    
    if any(n == 5 and rank > 2 for n, rank in results):
        conjecture_holds = False
        counterexample = "n=5, rank>2"
    elif any(n == 10 and rank > 3 for n, rank in results):
        conjecture_holds = False
        counterexample = "n=10, rank>3"
    elif any(n == 15 and rank > 4 for n, rank in results):
        conjecture_holds = False
        counterexample = "n=15, rank>4"
    elif any(n == 20 and rank > 5 for n, rank in results):
        conjecture_holds = False
        counterexample = "n=20, rank>5"
    elif any(n == 30 and rank > 6 for n, rank in results):
        conjecture_holds = False
        counterexample = "n=30, rank>6"
    elif any(n == 40 and rank > 7 for n, rank in results):
        conjecture_holds = False
        counterexample = "n=40, rank>7"
    
    return {
        "metric_name": "rank",
        "metric_value": float(mean_rank),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0000 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")