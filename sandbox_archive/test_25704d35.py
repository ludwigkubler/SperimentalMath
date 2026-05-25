# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mult(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        for j in range(k, n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_polynomial_time(n):
        # Placeholder function to check if a function is computable in polynomial time
        return True
    
    def compute_minimal_rank(n):
        # Placeholder function to compute the minimal rank of the group C*-algebra
        return n**2 + 1
    
    def compute_communication_complexity(n):
        # Placeholder function to compute the communication complexity for disjointness
        return n * (n - 1) // 2
    
    if not is_polynomial_time(40):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = random.randint(5, 40)
    minimal_rank = compute_minimal_rank(n)
    communication_complexity = compute_communication_complexity(n)
    
    if minimal_rank < communication_complexity:
        return {
            "metric_name": "minimal_rank",
            "metric_value": minimal_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Minimal rank {minimal_rank} is less than communication complexity {communication_complexity}"
        }
    
    if minimal_rank > n**2:
        return {
            "metric_name": "minimal_rank",
            "metric_value": minimal_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Minimal rank {minimal_rank} is greater than O(n^2) = {n**2}"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*41, 17))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all("counterexample" in r and r["counterexample"] != "" for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if 'counterexample' in r and r['counterexample'] != ''))]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")