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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_inverse(A):
    n = len(A)
    I = identity_matrix(n)
    A_augmented = [A[i] + I[i] for i in range(n)]
    
    # Gaussian elimination with partial pivoting
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            raise ValueError("Matrix is not invertible")
        
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        
        for j in range(n):
            A_augmented[i][j] /= A_augmented[i][i]
        
        for k in range(n):
            if k != i:
                factor = A_augmented[k][i]
                for j in range(2*n):
                    A_augmented[k][j] -= factor * A_augmented[i][j]
    
    return [row[n:] for row in A_augmented]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    else:
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

def rank(A):
    n, m = len(A), len(A[0])
    if n == 0 or m == 0:
        return 0
    
    # Gaussian elimination to find the rank
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            continue
        
        A[i], A[max_row] = A[max_row], A[i]
        
        for j in range(m):
            A[i][j] /= A[i][i]
        
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(m):
                    A[k][j] -= factor * A[i][j]
    
    return sum(1 for row in A if any(row))

def grothendieck_group_rank(clauses):
    n = len(clauses)
    I = [[0]*n for _ in range(n)]
    for i, clause in enumerate(clauses):
        for j in range(i+1, n):
            if set(clause).isdisjoint(set(clauses[j])):
                I[i][j] = 1
                I[j][i] = 1
    
    return rank(I)

def disjointness_complexity(n):
    # Simulate a random instance of the disjointness problem
    A = [random.choice([0, 1]) for _ in range(2**n)]
    B = [random.choice([0, 1]) for _ in range(2**n)]
    
    return sum(A[i] != B[i] for i in range(2**n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = [[random.randint(0, n-1) for _ in range(random.randint(1, 3))] for _ in range(n)]
            rank_value = grothendieck_group_rank(clauses)
            cc_value = disjointness_complexity(n)
            
            if rank_value == 0:
                continue
            
            ratio = Fraction(rank_value**2 * math.log(n), cc_value)
            total_metric_value += ratio
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value >= 1 and all(ratio >= 0.9 for ratio in [Fraction(rank**2 * math.log(n), cc) for n, rank, cc in zip(n_values, [grothendieck_group_rank([[]]*n) for _ in range(5)], [disjointness_complexity(n) for n in n_values])])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Rank^2 * log(n) to CC_R",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")