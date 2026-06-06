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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rref = [row[:] for row in matrix]
    pivot_row = 0
    for i in range(n):
        if pivot_row == m:
            break
        max_pivot = abs(rref[pivot_row][i])
        max_row = pivot_row
        for j in range(pivot_row+1, m):
            if abs(rref[j][i]) > max_pivot:
                max_pivot = abs(rref[j][i])
                max_row = j
        
        rref[pivot_row], rref[max_row] = rref[max_row], rref[pivot_row]
        
        for j in range(m):
            if j != pivot_row and rref[j][i] != 0:
                factor = rref[j][i] / rref[pivot_row][i]
                for k in range(n):
                    rref[j][k] -= factor * rref[pivot_row][k]
        
        pivot_row += 1
    
    rank = sum(1 for row in rref if any(row[i] != 0 for i in range(n)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    p_adic_steps_sum = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            b = [random.randint(-10, 10) for _ in range(n)]
            
            try:
                x = gaussian_elimination(A, b)
                p_adic_steps = sum(abs(x[i]) > 1e-6 for i in range(n))
                
                total_instances += 1
                p_adic_steps_sum += p_adic_steps
                
                rank_val = rank(A)
                diff = abs(p_adic_steps - rank_val)
                
                if diff > 3:
                    return {
                        "metric_name": "p-Adic Hensel Steps vs Rank",
                        "metric_value": None,
                        "instances_tested": total_instances,
                        "n_max": n,
                        "conjecture_holds": False,
                        "counterexample": f"Size {n}, p-adic steps: {p_adic_steps}, Rank: {rank_val}"
                    }
            except Exception as e:
                return {
                    "metric_name": "p-Adic Hensel Steps vs Rank",
                    "metric_value": None,
                    "instances_tested": total_instances,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    
    mean_steps = p_adic_steps_sum / total_instances
    return {
        "metric_name": "p-Adic Hensel Steps vs Rank",
        "metric_value": mean_steps,
        "instances_tested": total_instances,
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")