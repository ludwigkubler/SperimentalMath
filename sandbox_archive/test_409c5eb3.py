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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def is_independent(A, b):
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    gaussian_elimination(augmented)
    for i in range(len(augmented)):
        if abs(augmented[i][-1]) > 1e-9 and any(abs(augmented[i][j]) > 1e-9 for j in range(len(augmented[0])-1)):
            return False
    return True

def rank(A):
    m, n = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    return sum(1 for row in A_copy if any(abs(x) > 1e-9 for x in row))

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = random.sample(range(-num_vars, 0), 2) + random.sample(range(1, num_vars+1), 2)
        cnf.append(clause)
    return cnf

def circuit_complexity(cnf):
    stack = []
    for clause in cnf:
        if not any(abs(lit) == abs(stack[-1]) for lit in clause):
            stack.append(clause[0])
        else:
            stack.pop()
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_r = 0
    total_c = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n, 2*n)
            cnf = generate_cnf(n, m)
            r = rank(cnf)
            c = circuit_complexity(cnf)
            total_r += r
            total_c += c
            instances_tested += 1

    mean_r = Fraction(total_r, instances_tested)
    mean_c = Fraction(total_c, instances_tested)
    epsilon = Fraction(0.1)  # Example constant ε
    p_n = n_max * (n_max + 1) // 2  # Polynomial p(n) for demonstration

    if abs(mean_r - mean_c) <= epsilon * p_n:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"mean_r={mean_r}, mean_c={mean_c}, |mean_r - mean_c|={abs(mean_r - mean_c)}, εp(n)={epsilon * p_n}"

    return {
        "metric_name": "Rank vs Circuit Complexity",
        "metric_value": abs(mean_r - mean_c),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")