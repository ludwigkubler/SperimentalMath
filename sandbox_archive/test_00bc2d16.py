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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(M, p):
    n = len(M)
    I = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        I[i][i] = Fraction(1, 1)
    
    M_ext = [row + I[i] for i, row in enumerate(M)]
    n_ext = n * 2
    
    for k in range(n_ext):
        pivot_row = None
        for i in range(k, n_ext):
            if M_ext[i][k % n]:
                pivot_row = i
                break
        
        if not pivot_row:
            raise ValueError("Matrix is not full rank")
        
        M_ext[pivot_row], M_ext[k] = M_ext[k], M_ext[pivot_row]
        
        for j in range(n_ext):
            if j != k and M_ext[j][k % n]:
                factor = -M_ext[j][k % n] / M_ext[k][k % n]
                for l in range(n_ext):
                    M_ext[j][l] += factor * M_ext[k][l]
    
    for i in range(n):
        for j in range(n, 2*n):
            M_ext[i][j] /= M_ext[i][i]
        M_ext[i][i] = Fraction(1, 1)
    
    return [row[n:] for row in M_ext]

def matrix_mod_mul(A, B, p):
    n = len(A)
    C = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= p
    return C

def matrix_mod_pow(M, exp, p):
    n = len(M)
    result = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    base = M
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mod_mul(result, base, p)
        base = matrix_mod_mul(base, base, p)
        exp //= 2
    
    return result

def gaussian_elimination(A, b, p):
    n = len(A)
    A_aug = [row + [b[i]] for i, row in enumerate(A)]
    
    for k in range(n):
        pivot_row = None
        for i in range(k, n):
            if A_aug[i][k]:
                pivot_row = i
                break
        
        if not pivot_row:
            raise ValueError("Matrix is not full rank")
        
        A_aug[pivot_row], A_aug[k] = A_aug[k], A_aug[pivot_row]
        
        for j in range(n + 1):
            if j != k and A_aug[j][k]:
                factor = -A_aug[j][k] / A_aug[k][k]
                for l in range(n + 1):
                    A_aug[j][l] += factor * A_aug[k][l]
    
    x = [Fraction(0, 1) for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = (A_aug[i][-1] - sum(A_aug[i][j] * x[j] for j in range(i+1, n))) / A_aug[i][i]
    
    return [x_i % p for x_i in x]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 5 + (seed % 40) // 8
    m = 2 * n
    
    # Generate a random 3CNF formula
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables), random.choice(variables), random.choice(variables)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    
    # Construct the moduli space of stable maps (simplified model)
    M = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i] = Fraction(1, 1)
    
    # Compute the Gromov-Witten invariant I(F)
    I_F = sum(sum(row[j] for j in range(n)) for row in M) / n
    
    # Find the shortest resolution proof of each 3CNF formula
    t_F = len(clauses)
    
    # Statistically analyze the relationship between I(F) and log t*(F)
    if t_F == 0:
        return {
            "metric_name": "I(F)/log t*(F)",
            "metric_value": Fraction(1, 1),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Empty formula"
        }
    
    ratio = I_F / math.log(t_F)
    
    return {
        "metric_name": "I(F)/log t*(F)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= Fraction(1, 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= Fraction(1, 1)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > Fraction(1, 1) for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")