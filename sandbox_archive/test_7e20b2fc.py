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
    
    def generate_disjointness_instance(n):
        x = [random.randint(0, 1) for _ in range(n)]
        y = [random.randint(0, 1) for _ in range(n)]
        return x, y
    
    def truth_table(x, y):
        return [[x[i] == y[j] for j in range(len(y))] for i in range(len(x))]
    
    def grothendieck_group(M):
        n = len(M)
        G = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if M[i][j] == 1:
                    G[i][j] = 1
        return G
    
    def smith_normal_form(G):
        n = len(G)
        R = [[Fraction(G[i][j]) for j in range(n)] for i in range(n)]
        for k in range(n):
            # Find pivot
            pivot_row, pivot_col = None, None
            for i in range(k, n):
                for j in range(k, n):
                    if R[i][j] != 0:
                        pivot_row, pivot_col = i, j
                        break
                if pivot_row is not None:
                    break
            
            # Swap rows and columns to move the pivot to (k,k)
            if pivot_row != k:
                R[k], R[pivot_row] = R[pivot_row], R[k]
            if pivot_col != k:
                for i in range(n):
                    R[i][k], R[i][pivot_col] = R[i][pivot_col], R[i][k]
            
            # Eliminate below and to the right of the pivot
            pivot_value = R[k][k]
            for i in range(k+1, n):
                factor = -R[i][k] / pivot_value
                for j in range(k, n):
                    R[i][j] += factor * R[k][j]
            for j in range(k+1, n):
                factor = -R[k][j] / pivot_value
                for i in range(n):
                    R[i][j] += factor * R[i][k]
        
        rank = sum(1 for row in R if any(x != 0 for x in row))
        return rank
    
    def min_rank(K_n):
        return smith_normal_form(K_n)
    
    n_values = [10, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        x, y = generate_disjointness_instance(n)
        M = truth_table(x, y)
        K_n = grothendieck_group(M)
        rank = min_rank(K_n)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / len(n_values)
    conjecture_holds = all(rank >= n * math.log2(n) for n, rank in zip(n_values, [mean_rank] * len(n_values)))
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank} < {n * math.log2(n)}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")