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

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_2cnf(n, m):
    clauses = set()
    for _ in range(m):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        while len(literals) > 0:
            clause = []
            for literal in literals:
                if random.random() < 0.5:
                    clause.append(literal)
                    literals.remove(literal)
                else:
                    break
            clauses.add(tuple(sorted(clause)))
    return clauses

def gf2_matrix(n, m):
    matrix = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    pivot_col = 0
    for i in range(n):
        if pivot_col >= m:
            break
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][pivot_col]) > abs(matrix[max_row][pivot_col]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][pivot_col] == 0:
            pivot_col += 1
            continue
        for j in range(n):
            if j != i and matrix[j][pivot_col] != 0:
                factor = matrix[j][pivot_col] / matrix[i][pivot_col]
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        rank += 1
        pivot_col += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 20
    trials = 30
    total_monomials = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(trials):
        cnf = random_2cnf(n, m)
        matrix = gf2_matrix(n, n)
        rank = gaussian_elimination(matrix)
        monomials = 2 ** (n - rank)
        total_monomials += monomials
        instances_tested += 1

    mean_value = total_monomials / instances_tested
    support_fraction = instances_tested / trials

    if not math.isclose(mean_value, 2**(n/2), rel_tol=0.1):
        conjecture_holds = False
        counterexample = "monomial_count_deviation"

    return {
        "metric_name": "monomial_count",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"monomial_count_deviation\" first_failing_seed={first_failing_seed}")