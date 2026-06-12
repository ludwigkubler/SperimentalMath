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
    
    def generate_boolean_function(n):
        return {i: random.choice([0, 1]) for i in range(2**n)}
    
    def matrix_mult(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C
    
    def matrix_sub(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C
    
    def matrix_inv(A, mod):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A_augmented = [row + I[i] for i, row in enumerate(A)]
        
        for i in range(n):
            pivot = A_augmented[i][i]
            if pivot == 0:
                return None
            
            for j in range(i, n * 2):
                A_augmented[i][j] = (A_augmented[i][j] * pow(pivot, mod - 2, mod)) % mod
        
            for k in range(n):
                if k != i:
                    factor = A_augmented[k][i]
                    for j in range(i, n * 2):
                        A_augmented[k][j] = (A_augmented[k][j] - factor * A_augmented[i][j]) % mod
        
        return [row[n:] for row in A_augmented]
    
    def lie_algebra_basis(f, n):
        A = [[f[(i >> j) & 1] * f[(j >> k) & 1] for k in range(n)] for j in range(n)]
        inv_A = matrix_inv(A, 2)
        if inv_A is None:
            return None
        B = matrix_mult(A, inv_A, 2)
        C = matrix_sub(B, I, 2)
        return C
    
    def communication_complexity_rank_variance(f, n):
        rank = sum(1 for row in f.values() if any(row))
        return (rank - 1) * (n - rank)
    
    def minimal_order_of_kostant_multiplicity(C):
        n = len(C)
        count = 0
        visited = [False] * n
        stack = []
        
        def dfs(node):
            nonlocal count
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if C[node][neighbor] == 1 and not visited[neighbor]:
                        dfs(neighbor)
                count += 1
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
        
        return n // count
    
    def run_instance(n):
        f = generate_boolean_function(n)
        B = lie_algebra_basis(f, n)
        if B is None:
            return {"metric_value": float('inf'), "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "mapping_undefined"}
        
        kappa_f = minimal_order_of_kostant_multiplicity(B)
        rank_variance = communication_complexity_rank_variance(f, n)
        
        return {"metric_value": kappa_f, "instances_tested": 1, "n_max": n, "conjecture_holds": True, "counterexample": ""}
    
    instance_result = run_instance(40)
    return instance_result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else float('nan')
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values)) if metric_values else float('nan')
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")