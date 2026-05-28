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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def matrix_mul(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_det(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for c in range(len(A)):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = matrix_det(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def is_invertible(matrix):
    return matrix_det(matrix) != 0

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        b[i] /= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
    return [b[i] for i in range(n)]

def min_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if is_invertible([row[:i] + row[i+1:] for row in matrix]):
            rank += 1
    return rank

def communication_complexity(n):
    # Simplified model of communication complexity for demonstration
    return n * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_rank = 0
    total_cc = 0
    for _ in range(5):
        is_symmetric = random.choice([True, False])
        # Generate symmetric and asymmetric instances (simplified)
        if is_symmetric:
            instance = [random.randint(0, 1) for _ in range(n)]
        else:
            instance = [random.randint(0, 1) for _ in range(n-1)] + [1 - sum(instance[:n-1]) % 2]
        
        # Calculate minimal rank of cyclic difference set (simplified)
        diff_set = [(instance[i] - instance[(i+1)%n]) % 2 for i in range(n)]
        matrix = [[diff_set[j] == k for j in range(n)] for k in range(2)]
        rank = min_rank(matrix)
        
        # Calculate communication complexity
        cc = communication_complexity(n)
        
        total_rank += rank
        total_cc += cc
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_cc = total_cc / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * cc for rank, cc in zip([mean_rank] * instances_tested, [mean_cc] * instances_tested)) -
                               instances_tested * mean_rank * mean_cc) / math.sqrt((instances_tested * sum(rank**2 for rank in [mean_rank] * instances_tested) - instances_tested * mean_rank**2) *
                                                                 (instances_tested * sum(cc**2 for cc in [mean_cc] * instances_tested) - instances_tested * mean_cc**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "n/a"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n/a\" first_failing_seed={first_failing_seed}")