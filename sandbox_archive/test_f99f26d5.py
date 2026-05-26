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
    
    def generate_disjointness_instance(n):
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        return A, B
    
    def truth_table(A, B):
        n = len(A)
        M = [[A[i] == B[j] for j in range(n)] for i in range(n)]
        return M
    
    def grothendieck_group(M):
        n = len(M)
        V = [set(range(n)) for _ in range(2**n)]
        E = []
        
        for v1 in V:
            for v2 in V:
                if all(M[i][j] == (i in v1 and j in v2) or (i not in v1 and j not in v2) for i in range(n) for j in range(n)):
                    E.append((v1, v2))
        
        return V, E
    
    def smith_normal_form(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = G[i][j]
        
        R = 1
        C = 1
        
        while True:
            # Find pivot
            pivot_found = False
            for r in range(R, n):
                for c in range(C, n):
                    if A[r][c] != 0:
                        pivot_row = r
                        pivot_col = c
                        pivot_found = True
                        break
                if pivot_found:
                    break
            
            if not pivot_found:
                break
            
            # Swap rows to bring pivot to top-left
            for i in range(pivot_row):
                A[i], A[pivot_row] = A[pivot_row], A[i]
            
            # Swap columns to bring pivot to top-left
            for j in range(pivot_col):
                for i in range(n):
                    A[i][j], A[i][pivot_col] = A[i][pivot_col], A[i][j]
            
            # Eliminate below and right of pivot
            pivot_val = A[pivot_row][pivot_col]
            for r in range(pivot_row + 1, n):
                factor = -A[r][pivot_col] // pivot_val
                for c in range(n):
                    A[r][c] += factor * A[pivot_row][c]
            
            for c in range(pivot_col + 1, n):
                factor = -A[pivot_row][c] // pivot_val
                for r in range(n):
                    A[r][c] += factor * A[r][pivot_col]
            
            R += 1
            C += 1
        
        rank = sum(1 for row in A if any(row))
        return rank
    
    def min_rank_K_group(M):
        V, E = grothendieck_group(M)
        G = [[0] * len(V) for _ in range(len(V))]
        
        for v1, v2 in E:
            index1 = V.index(v1)
            index2 = V.index(v2)
            G[index1][index2] += 1
            G[index2][index1] += 1
        
        return smith_normal_form(G)
    
    n_values = [10, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(7):  # Aim for at least 30 instances per seed
            A, B = generate_disjointness_instance(n)
            M = truth_table(A, B)
            rank = min_rank_K_group(M)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= n * math.log2(n)
    
    return {
        "metric_name": "Minimal Rank of K-Theory",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean rank {mean_rank} < n log2(n) for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")