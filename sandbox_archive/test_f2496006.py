# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import combinations, permutations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def inverse_kostka(K, n):
    K_inv = [[0] * n for _ in range(n)]
    for i in range(n):
        K_inv[i][i] = 1 / K[i][i]
        for j in range(i + 1, n):
            factor = K[j][i] / K[i][i]
            for k in range(n):
                K_inv[j][k] -= factor * K_inv[i][k]
    return K_inv

def schur_defect(v, n):
    lambda_v = sorted(v)
    partitions = []
    def generate_partitions(k, current_partition):
        if len(current_partition) == n:
            if sum(current_partition) == k:
                partitions.append(tuple(sorted(current_partition)))
            return
        for i in range(current_partition[-1] if current_partition else 0, k + 1):
            generate_partitions(k - i, current_partition + [i])
    generate_partitions(sum(v), [])
    
    K = [[0] * len(partitions) for _ in range(len(partitions))]
    for i, mu in enumerate(partitions):
        for j, lambda_v_i in enumerate(lambda_v):
            count = sum(1 for k in range(n) if partitions[i][k] >= lambda_v_i)
            K[i][j] += 1
    
    K_inv = inverse_kostka(K, len(partitions))
    defect = sum(max(0, -K_inv[i][j]) for i in range(len(partitions)) for j in range(len(lambda_v)))
    return defect

def lex_dpll(F):
    n = len(F)
    stack = []
    assignment = [None] * n
    def backtrack():
        if all(assignment[i] is not None for i in range(n)):
            return True
        var = next(i for i in range(n) if assignment[i] is None)
        for val in (0, 1):
            assignment[var] = val
            stack.append((var, val))
            if all(F[i][j] <= assignment[j] for j in range(n)):
                if backtrack():
                    return True
            stack.pop()
            assignment[var] = None
        return False
    return backtrack()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6, 7, 8, 9]
    results = []
    
    for n in n_values:
        F = [[random.randint(0, 1) for _ in range(n)] for _ in range(n + 1)]
        v = [sum(F[i][j] for i in range(n + 1)) for j in range(n)]
        lambda_v = sorted(v)
        
        partitions = []
        def generate_partitions(k, current_partition):
            if len(current_partition) == n:
                if sum(current_partition) == k:
                    partitions.append(tuple(sorted(current_partition)))
                return
            for i in range(current_partition[-1] if current_partition else 0, k + 1):
                generate_partitions(k - i, current_partition + [i])
        generate_partitions(sum(v), [])
        
        K = [[0] * len(partitions) for _ in range(len(partitions))]
        for i, mu in enumerate(partitions):
            for j, lambda_v_i in enumerate(lambda_v):
                count = sum(1 for k in range(n) if partitions[i][k] >= lambda_v_i)
                K[i][j] += 1
        
        K_inv = inverse_kostka(K, len(partitions))
        defect = sum(max(0, -K_inv[i][j]) for i in range(len(partitions)) for j in range(len(lambda_v)))
        
        L_TF = lex_dpll(F)
        if not L_TF:
            return {
                "metric_name": "log2(L_TF)",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "L_TF is falsified"
            }
        
        log2_L_TF = math.log2(L_TF)
        results.append((n, log2_L_TF, defect))
    
    mean_log2_L_TF = sum(log2_L_TF for _, log2_L_TF, _ in results) / len(results)
    std_log2_L_TF = math.sqrt(sum((log2_L_TF - mean_log2_L_TF) ** 2 for _, log2_L_TF, _ in results) / len(results))
    support_fraction = sum(1 for _, log2_L_TF, defect in results if log2_L_TF >= (defect + 1) / 4) / len(results)
    
    return {
        "metric_name": "log2(L_TF)",
        "metric_value": mean_log2_L_TF,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
    
    results = [run_trial(seed) for seed in seeds]
    mean_log2_L_TF = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_log2_L_TF = math.sqrt(sum((result["metric_value"] - mean_log2_L_TF) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_log2_L_TF} std={std_log2_L_TF} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"L_TF is falsified\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")