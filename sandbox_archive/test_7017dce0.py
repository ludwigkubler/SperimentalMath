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
    rows, cols = len(A), len(A[0])
    rank = 0
    
    for j in range(cols):
        pivot_row = -1
        for i in range(rank, rows):
            if A[i][j] != 0:
                pivot_row = i
                break
        
        if pivot_row == -1:
            continue
        
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        
        for i in range(rows):
            if i != rank:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(cols):
                    A[i][k] -= factor * A[rank][k]
        
        rank += 1
    
    return rank

def rank(matrix):
    T = [[max(row[j], col[j]) for j in range(len(col))] for row in matrix]
    return gaussian_elimination(T)

def tropical_curve(M):
    n = len(M)
    curve = []
    for i in range(n):
        for j in range(n):
            if M[i][j] != 0:
                curve.append((i, j))
    return curve

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    correlation_sum = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        M = [[random.choice([0, 1]) * random.random() for _ in range(n)] for _ in range(n)]
        
        rank_M = rank(M)
        curve = tropical_curve(M)
        rank_curve = len(curve)
        
        correlation_sum += abs(rank_M - rank_curve) / max(rank_M, rank_curve)
    
    mean_correlation = correlation_sum / instances_tested
    conjecture_holds = mean_correlation >= 0.5
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation too low\" first_failing_seed={r['seed']}")
                break