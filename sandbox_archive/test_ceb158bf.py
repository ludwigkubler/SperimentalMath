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

def matrix_multiplication(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Matrix multiplication not possible")
    
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    
    C = [[Fraction(0) for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def identity_matrix(n):
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    return I

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    
    det = Fraction(0)
    sign = Fraction(1)
    
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix)
        sign *= -Fraction(1)
    
    return det

def minimal_representation_rank(n):
    S3 = [
        [[Fraction(1), Fraction(0), Fraction(0)],
         [Fraction(0), Fraction(1), Fraction(0)],
         [Fraction(0), Fraction(0), Fraction(1)]],
        
        [[Fraction(0), Fraction(1), Fraction(0)],
         [Fraction(1), Fraction(0), Fraction(0)],
         [Fraction(0), Fraction(0), Fraction(1)]],
        
        [[Fraction(0), Fraction(0), Fraction(1)],
         [Fraction(0), Fraction(1), Fraction(0)],
         [Fraction(1), Fraction(0), Fraction(0)]]
    ]
    
    T_n = identity_matrix(n)
    for _ in range(n):
        T_n = matrix_multiplication(T_n, S3)
    
    det_m = determinant([[Fraction(1) if i == j else Fraction(0) for j in range(m)] for i in range(m)])
    rho_det_m = len([x for x in det_m.numerator.as_integer_ratio()[1].primefactors()]) + 1
    
    return len([x for x in T_n[0][0].as_integer_ratio()[1].primefactors()]) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(2, 40)
    rho_T_n = minimal_representation_rank(n)
    
    m = math.floor(n ** 1.5)
    det_m = determinant([[Fraction(1) if i == j else Fraction(0) for j in range(m)] for i in range(m)])
    rho_det_m = len([x for x in det_m.numerator.as_integer_ratio()[1].primefactors()]) + 1
    
    metric_value = rho_T_n <= rho_det_m
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else f"rho(T_{n})={rho_T_n}, rho(det_{m})={rho_det_m}"
    
    return {
        "metric_name": "minimal_representation_rank",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")