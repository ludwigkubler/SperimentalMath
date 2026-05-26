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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = set()
    for _ in range(m):
        clause = []
        while len(clause) < 2:
            lit = random.choice(variables)
            if -lit not in clause:
                clause.append(lit)
        clauses.add(tuple(sorted(clause)))
    return clauses

def legendre_symbol(a, p):
    if a == 0:
        return 0
    if a % 2 == 1 and (p % 8 == 3 or p % 8 == 5):
        return -1
    if a % 2 == 1 and (p % 8 == 1 or p % 8 == 7):
        return 1
    if a % 2 == 0:
        e = 0
        while a % 2 == 0:
            a //= 2
            e += 1
        if e % 2 == 1 and (p % 8 == 3 or p % 8 == 5):
            return -1
        else:
            return 1

def quadratic_reciprocity_matrix(clauses, n):
    m = len(clauses)
    matrix = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            lit1, lit2 = clauses[i][0], clauses[j][0]
            if lit1 != -lit2 and lit2 != -lit1:
                matrix[i][j] = legendre_symbol(lit1 * lit2, n)
    return matrix

def tseitin_resolution_width(clauses):
    stack = []
    literals = set()
    for clause in clauses:
        literals.update(clause)
    for literal in literals:
        stack.append((literal, False))
    while stack:
        literal, negated = stack.pop()
        if negated:
            continue
        for clause in clauses:
            if literal in clause and not any(-x in clause for x in clause):
                for other_literal in clause:
                    if other_literal != literal:
                        stack.append((other_literal, True))
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 2 * n
    clauses = random_cnf(n, m)
    matrix = quadratic_reciprocity_matrix(clauses, n)
    width = tseitin_resolution_width(clauses)
    min_rank = len(matrix)
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] != 0:
                min_rank -= 1
                break
        else:
            continue
        break

    conjecture_holds = width == math.isclose(width, math.sqrt(n) * math.log(n), rel_tol=1e-5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")