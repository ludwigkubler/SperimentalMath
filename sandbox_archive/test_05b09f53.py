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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(m)]
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    for k in range(n):
        pivot_row = k
        for i in range(k + 1, m):
            if abs(A[i][k]) > abs(A[pivot_row][k]):
                pivot_row = i
        A[k], A[pivot_row] = A[pivot_row], A[k]
        b[k], b[pivot_row] = b[pivot_row], b[k]
        for i in range(k + 1, m):
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
            b[i] -= factor * b[k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def coxeter_reflections(permutation):
    n = len(permutation)
    reflections = []
    for i in range(n):
        if permutation[i] != i:
            j = permutation.index(i)
            reflection = [j if k == i else i if k == j else k for k in range(n)]
            reflections.append(reflection)
    return reflections

def entanglement_complexity(circuit):
    n = len(circuit)
    complexity = 0
    for i in range(n):
        for j in range(i + 1, n):
            if circuit[i] != circuit[j]:
                complexity += 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        permutations = [list(range(n)) for _ in range(10)]
        reflections = [coxeter_reflections(p) for p in permutations]
        entanglement_values = [entanglement_complexity(c) for c in permutations]
        
        if not all(reflections):
            return {
                "metric_name": "Coxeter Reflections",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        for i in range(len(permutations)):
            if len(reflections[i]) != entanglement_values[i]:
                return {
                    "metric_name": "Coxeter Reflections",
                    "metric_value": None,
                    "instances_tested": 0,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Instance {i}: Reflections={len(reflections[i])}, Entanglement={entanglement_values[i]}"
                }
        
        results.extend(reflections)
    
    if not results:
        return {
            "metric_name": "Coxeter Reflections",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_reflections = sum(len(r) for r in results) / len(results)
    std_reflections = math.sqrt(sum((len(r) - mean_reflections) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(len(r) - entanglement_complexity(random.sample(range(n), n))) <= 5) / len(results)
    
    return {
        "metric_name": "Coxeter Reflections",
        "metric_value": mean_reflections,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")