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

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * (matrix[1][2] - matrix[2][1])
    inv_det = mod_inverse(det, mod)
    adjugate = [[(matrix[(i+1) % n][(j+1) % n] - matrix[(i+1) % n][(j+2) % n]) * (matrix[(i+2) % n][(j+1) % n] - matrix[(i+2) % n][(j+2) % n]) for j in range(n)] for i in range(n)]
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_mul(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_pow(matrix, n):
    if n == 1:
        return matrix
    elif n % 2 == 0:
        half = matrix_pow(matrix, n // 2)
        return matrix_mul(half, half)
    else:
        return matrix_mul(matrix, matrix_pow(matrix, n - 1))

def dpll_width(cnf):
    # Simplified DPLL algorithm to estimate width
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
        pure_literals = [l for l in range(1, len(cnf) + 1) if all(l in c or -l in c for c in clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                new_assignment[literal] = False
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                else:
                    return False
        literal = random.choice(range(1, len(cnf) + 1))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False

    assignment = [False] * (len(cnf) + 1)
    return len(dpll(cnf, assignment))

def generate_cnf(n):
    cnf = []
    for i in range(1, n + 1):
        clause = random.sample(range(1, n + 1), 3)
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_width = 0
        for _ in range(5):  # Sample 5 instances per n
            cnf = generate_cnf(n)
            width = dpll_width(cnf)
            results.append((n, width))
            instances_tested += 1
            total_width += width
    mean_width = sum(width for _, width in results) / len(results)
    conjecture_holds = all(width >= 2**n for n, width in results if n <= math.log(len(results), 2))
    counterexample = "" if conjecture_holds else "width < 2^n for some n"
    return {
        "metric_name": "DPLL Width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width:.2f} std=... support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='width < 2^n for some n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")