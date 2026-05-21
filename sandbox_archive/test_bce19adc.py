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

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mult(A, B, p):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= p
    return C

def gaussian_elimination(A, b, p):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    
    for j in range(n):
        max_row = j
        for i in range(j+1, n):
            if abs(Augmented[i][j]) > abs(Augmented[max_row][j]):
                max_row = i
        
        Augmented[j], Augmented[max_row] = Augmented[max_row], Augmented[j]
        
        pivot = Augmented[j][j]
        for k in range(j, n+1):
            Augmented[j][k] *= mod_inverse(pivot, p)
            Augmented[j][k] %= p
        
        for i in range(n):
            if i != j:
                factor = Augmented[i][j]
                for k in range(j, n+1):
                    Augmented[i][k] -= factor * Augmented[j][k]
                    Augmented[i][k] %= p
    
    return [row[-1] for row in Augmented]

def noncommutative_rank(M, p):
    n = len(M)
    rank = 0
    for i in range(n):
        if any(M[i][j] != 0 for j in range(i, n)):
            rank += 1
            pivot_row = i
            for j in range(n):
                if M[j][pivot_row] != 0:
                    M[j], M[pivot_row] = M[pivot_row], M[j]
                    break
            for j in range(n):
                if j != pivot_row:
                    factor = M[j][pivot_row]
                    for k in range(n):
                        M[j][k] -= factor * M[pivot_row][k]
    return rank

def generate_bp(n, read_twice):
    bp = []
    for i in range(n):
        if random.choice([True, False]) or read_twice:
            bp.append(random.randint(0, n-1))
        else:
            bp.append(bp[-1])
    return bp

def tensor_product(bp1, bp2):
    n = len(bp1)
    M = [[0] * (n*n) for _ in range(n*n)]
    for i in range(n):
        for j in range(n):
            M[i*n+j][bp1[i]*n+bp2[j]] = 1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    p = 101
    
    read_once_bp = generate_bp(n, False)
    read_twice_bp = generate_bp(n, True)
    
    M_read_once = tensor_product(read_once_bp, read_once_bp)
    M_read_twice = tensor_product(read_twice_bp, read_twice_bp)
    
    rank_read_once = noncommutative_rank(M_read_once, p)
    rank_read_twice = noncommutative_rank(M_read_twice, p)
    
    metric_value_read_once = math.log(rank_read_once + 1) / math.log(n)
    metric_value_read_twice = math.log(rank_read_twice + 1) / math.log(n)
    
    conjecture_holds_read_once = rank_read_once <= math.log(n, 2)
    conjecture_holds_read_twice = rank_read_twice >= n
    
    return {
        "metric_name": "Noncommutative Rank",
        "metric_value_read_once": metric_value_read_once,
        "metric_value_read_twice": metric_value_read_twice,
        "instances_tested": 1,
        "conjecture_holds_read_once": conjecture_holds_read_once,
        "conjecture_holds_read_twice": conjecture_holds_read_twice,
        "counterexample_read_once": "" if conjecture_holds_read_once else str(read_once_bp),
        "counterexample_read_twice": "" if conjecture_holds_read_twice else str(read_twice_bp)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_value_read_once\": {result['metric_value_read_once']:.6f}, \"metric_value_read_twice\": {result['metric_value_read_twice']:.6f}, \"conjecture_holds_read_once\": {result['conjecture_holds_read_once']}, \"conjecture_holds_read_twice\": {result['conjecture_holds_read_twice']}, \"counterexample_read_once\": \"{result['counterexample_read_once']}\", \"counterexample_read_twice\": \"{result['counterexample_read_twice']}\"}}")
        results.append(result)
    
    mean_read_once = sum(res['metric_value_read_once'] for res in results) / len(results)
    std_read_once = math.sqrt(sum((res['metric_value_read_once'] - mean_read_once) ** 2 for res in results) / len(results))
    support_fraction_read_once = sum(1 for res in results if res['conjecture_holds_read_once']) / len(results)
    
    mean_read_twice = sum(res['metric_value_read_twice'] for res in results) / len(results)
    std_read_twice = math.sqrt(sum((res['metric_value_read_twice'] - mean_read_twice) ** 2 for res in results) / len(results))
    support_fraction_read_twice = sum(1 for res in results if res['conjecture_holds_read_twice']) / len(results)
    
    if support_fraction_read_once >= 0.8:
        print(f"RESULT: SUPPORTED mean_read_once={mean_read_once:.6f} std_read_once={std_read_once:.6f} support_fraction_read_once={support_fraction_read_once:.2f}")
    elif any(res['counterexample_read_once'] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if res['counterexample_read_once'])
        print(f"RESULT: FALSIFIED counterexample_read_once=\"{results[first_failing_seed]['counterexample_read_once']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_read_once_too_low")
    
    if support_fraction_read_twice >= 0.8:
        print(f"RESULT: SUPPORTED mean_read_twice={mean_read_twice:.6f} std_read_twice={std_read_twice:.6f} support_fraction_read_twice={support_fraction_read_twice:.2f}")
    elif any(res['counterexample_read_twice'] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if res['counterexample_read_twice'])
        print(f"RESULT: FALSIFIED counterexample_read_twice=\"{results[first_failing_seed]['counterexample_read_twice']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_read_twice_too_low")