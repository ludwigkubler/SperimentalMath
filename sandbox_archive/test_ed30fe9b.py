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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_norm(A, p):
        n = len(A)
        norm = 0
        for i in range(1, n+1):
            for j in range(1, n+1):
                if i + j - 2 == n:
                    norm += abs(A[i-1][j-1])**p
        return norm**(1/p)
    
    def generate_entanglement_matrix(n):
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A[i][j] = random.random()
                A[j][i] = A[i][j]
        return gaussian_elimination(A)
    
    def disjointness_communication_complexity(n):
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    c = 1.0  # Placeholder value for constant c
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random matrices
            M = generate_entanglement_matrix(n)
            norm = matrix_norm(M, float('inf'))
            instances_tested += 1
            total_metric_value += norm
            if norm < c * n:
                conjecture_holds = False
                counterexample = f"n={n}, norm={norm} < {c}*{n}"
                break
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0 if conjecture_holds else 0.0
    
    return {
        "metric_name": "Noncommutative L_p Norm",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")