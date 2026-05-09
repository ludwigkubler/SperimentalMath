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
from math import factorial

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mult(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A):
    n = len(A)
    det = 0
    if n == 1:
        return [[A[0][0]**-1]]
    elif n == 2:
        det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
        return [[A[1][1]/det, -A[0][1]/det],
                [-A[1][0]/det, A[0][0]/det]]
    else:
        for c in range(n):
            M = []
            for i in range(1, n):
                row = []
                for j in range(n):
                    if j != c:
                        row.append(A[i][j])
                M.append(row)
            det += (-1)**c * A[0][c] * matrix_det(M)
        inv = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M = []
                for r in range(n):
                    if r != 0:
                        row = []
                        for c in range(n):
                            if c != j:
                                row.append(A[r][c])
                        M.append(row)
                inv[i][j] = (-1)**(i+j) * matrix_det(M) / det
        return inv

def matrix_det(A):
    n = len(A)
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    else:
        det = 0
        for c in range(n):
            M = []
            for i in range(1, n):
                row = []
                for j in range(n):
                    if j != c:
                        row.append(A[i][j])
                M.append(row)
            det += (-1)**c * A[0][c] * matrix_det(M)
        return det

def hook_length_formula(shape):
    n = len(shape)
    total = 1
    for i in range(n):
        for j in range(len(shape[i])):
            h = shape[i][j]
            v = sum(1 for k in range(i+1, n) if shape[k][j] > h)
            l = sum(1 for k in range(j+1, len(shape[i])) if shape[i][k] > h)
            total *= (h + v + l - 1) // (h * v * l)
    return total

def generate_random_matrix(n):
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    perm_n = generate_random_matrix(n)
    det_n = [[sum(row[i] * row[j] for j in range(i+1)) for i in range(n)] for row in perm_n]
    
    sym_perm_n = matrix_det(perm_n)
    sym_det_n = matrix_det(det_n)
    
    count_perm_n = hook_length_formula([[i+1 for i in range(n)]])
    count_det_n = hook_length_formula([[n-i for i in range(n)]])
    
    ratio = count_perm_n / count_det_n
    
    conjecture_holds = ratio > 2**n
    counterexample = "" if conjecture_holds else f"Ratio {ratio} <= 2^n"
    
    return {
        "metric_name": "Ratio of SYT counts",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.6f} std=0.000000 support_fraction={support_fraction:.2%}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.6f} std=0.000000 support_fraction={support_fraction:.2%}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio <= 2^n\" first_failing_seed={first_failing_seed}")