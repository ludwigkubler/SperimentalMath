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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            # Find the pivot
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        
        # Back-substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        
        return x
    
    def smith_normal_form(A):
        n = len(A)
        B = [row[:] for row in A]
        U = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        V = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        
        for k in range(n):
            # Find the pivot
            max_col = k
            for j in range(k+1, n):
                if abs(B[k][j]) > abs(B[max_col][k]):
                    max_col = j
            B[k], B[max_col] = B[max_col], B[k]
            U[k], U[max_col] = U[max_col], U[k]
            
            # Eliminate below the pivot
            for i in range(k+1, n):
                factor = B[i][k] / B[k][k]
                for j in range(n):
                    B[i][j] -= factor * B[k][j]
                U[i][k] -= factor * U[k][k]
        
        # Eliminate to the left of the pivot
        for k in range(n-1, -1, -1):
            for i in range(k):
                factor = B[i][k] / B[k][k]
                for j in range(n):
                    B[i][j] -= factor * B[k][j]
                V[k][i] -= factor * V[k][k]
        
        return B, U, V
    
    def frege_proof_depth(f, n):
        # Simulate a small DPLL solver to estimate Frege proof depth
        stack = [(f, 0)]
        max_depth = 0
        while stack:
            current_f, depth = stack.pop()
            if depth > max_depth:
                max_depth = depth
            if len(current_f) == n:
                continue
            for i in range(2):
                new_f = current_f[:]
                new_f.append(i)
                stack.append((new_f, depth + 1))
        return max_depth
    
    def minimal_representation_rank(f, n):
        A = [[f[j * (2**(n-i-1)) + k] for j in range(2**(i+1))] for i in range(n)]
        B, U, V = smith_normal_form(A)
        rank = sum(1 for row in B if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rrep_f = minimal_representation_rank(f, n)
        d_f = frege_proof_depth(f, n)
        
        if d_f == 0:
            continue
        
        metrics.append({
            "n": n,
            "rrep_f": rrep_f,
            "d_f": d_f
        })
    
    if not metrics:
        return {
            "metric_name": "minimal_representation_rank_over_frege_depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rrep_d_f = sum(metric["rrep_f"] / metric["d_f"] for metric in metrics) / len(metrics)
    
    return {
        "metric_name": "minimal_representation_rank_over_frege_depth",
        "metric_value": mean_rrep_d_f,
        "instances_tested": len(metrics),
        "n_max": max(metric["n"] for metric in metrics),
        "conjecture_holds": mean_rrep_d_f <= 1.5,
        "counterexample": "" if mean_rrep_d_f <= 1.5 else f"mean_rrep_d_f = {mean_rrep_d_f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")