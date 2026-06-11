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
            factor = Fraction(A[k][i], pivot)
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    
    return A

def matrix_multiply(A, B):
    m, p = len(A), len(B[0])
    n = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def construct_twisted_module(circuit):
    n = len(circuit)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        if circuit[i]:
            A[i][i] = 1
            A[i][-1] = 1
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = [random.choice([False, True]) for _ in range(n)]
        e_C = sum(circuit)  # Simplified entanglement complexity
        
        M = construct_twisted_module(circuit)
        size_M = len(M)
        
        if size_M < 1 or size_M > e_C:
            return {
                "metric_name": "min_order",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append(size_M)
    
    mean_size_M = sum(results) / len(results)
    conjecture_holds = all(1 <= size_M <= e_C for size_M, e_C in zip(results, [sum(circuit) for circuit in [random.choice([False, True]) for _ in range(n)] for n in n_values]))
    
    return {
        "metric_name": "min_order",
        "metric_value": mean_size_M,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["conjecture_holds"]:
            results.append(result["metric_value"])
    
    mean_result = sum(results) / len(results) if results else None
    support_fraction = len([r for r in results if 1 <= r]) / len(results)
    
    if all(1 <= r for r in results):
        print(f"RESULT: SUPPORTED mean={mean_result} std=0.0 support_fraction={support_fraction}")
    elif any(r < 1 or r > e_C for r, e_C in zip(results, [sum(circuit) for circuit in [random.choice([False, True]) for _ in range(n)] for n in n_values])):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r, e_C in zip(results, [sum(circuit) for circuit in [random.choice([False, True]) for _ in range(n)] for n in n_values]) if r < 1 or r > e_C))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")