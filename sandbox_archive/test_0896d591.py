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
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b//a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inverse(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]
    return I

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monomial_ideal(n):
        generators = []
        for _ in range(random.randint(2, 5)):
            exponents = [random.randint(1, 3) for _ in range(n)]
            generators.append(tuple(exponents))
        return frozenset(generators)

    def k_theory_rank(generators):
        n = len(generators[0])
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0 for _ in range(n)]
        for gen in generators:
            for i in range(n):
                if gen[i] > 0:
                    A[i][i] += gen[i]
                    b[i] += gen[i]
        x = gaussian_elimination(A, b)
        rank = sum(1 for val in x if abs(val) > 1e-9)
        return rank

    def monotone_circuit_depth(generators):
        n = len(generators[0])
        depth = 0
        for gen in generators:
            current_depth = 0
            for exp in gen:
                current_depth += math.ceil(math.log2(exp + 1))
            depth = max(depth, current_depth)
        return depth

    instances_tested = 30
    total_rank = 0
    total_depth = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        ideal = generate_monomial_ideal(n)
        rank = k_theory_rank(ideal)
        depth = monotone_circuit_depth(ideal)
        total_rank += rank
        total_depth += depth
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_depth = Fraction(total_depth, instances_tested)
    
    ratio = mean_rank / mean_depth
    conjecture_holds = ratio <= 1
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > 1"
    
    return {
        "metric_name": "K-theory Rank / Circuit Depth",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] * r["instances_tested"] for r in results)
    total_depth = sum(1 / r["metric_value"] for r in results)
    mean_ratio = Fraction(total_rank, len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 1\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")