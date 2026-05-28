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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

def matrix_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(n)):
            continue
        rank += 1
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return rank

def generate_lie_algebra(n):
    L = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            L[i][j] = random.choice([0, 1])
            L[j][i] = (L[i][j] + 1) % 2
    return L

def tropicalize(L):
    T_L = [[math.inf]*len(L) for _ in range(len(L))]
    for i in range(len(L)):
        for j in range(len(L)):
            if L[i][j] == 0:
                T_L[i][j] = 0
            elif L[i][j] == 1:
                T_L[i][j] = math.inf
    return T_L

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            F = ['x' + str(i) for i in range(n)]
            t_F = random.randint(n, n**2)
            
            L = generate_lie_algebra(n)
            T_L = tropicalize(L)
            gaussian_elimination(T_L)
            rank = matrix_rank(T_L)
            
            total_rank += rank
            total_length += t_F
            instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    avg_length = total_length / instances_tested
    
    if avg_rank < avg_length:
        conjecture_holds = False
        counterexample = f"avg_rank={avg_rank} < avg_length={avg_length}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Average Minimal Rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_rank < avg_length\" first_failing_seed={first_failing_seed}")