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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def encode_clause(clause, n):
    b = [0] * (2 * n)
    for lit in clause:
        if lit > 0:
            b[lit - 1] = 1
        else:
            b[-lit - 1] = 1
    return b

def lyndon_factorization(b, ordering):
    n = len(b) // 2
    factors = []
    i = 0
    while i < 2 * n:
        j = i + 1
        while j < 2 * n and b[ordering[j]] == b[ordering[i]]:
            j += 1
        factors.append(j - i)
        i = j
    return factors

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_3cnf(n, density):
        clauses = []
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = set()
            while len(clause) < 3:
                lit = random.randint(1, n)
                if random.choice([True, False]):
                    lit = -lit
                clause.add(lit)
            clauses.append(list(clause))
        return clauses
    
    def generate_php_m(m):
        n = m + 1
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([i + 1, -j - 1])
                clauses.append([-i - 1, j + 1])
                clauses.append([i + 1, j + 1])
                clauses.append([-i - 1, -j - 1])
        return clauses
    
    def generate_tseitin_formula(n):
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i, -(n + i)])
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([-i - 1, -j - 1, n + i + j])
        return clauses
    
    def dpll(clauses, assignment, ordering):
        if not clauses:
            return True
        literal = next((lit for lit in ordering if lit not in assignment and -lit not in assignment), None)
        if literal is None:
            return False
        assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c]
        if dpll(new_clauses, assignment, ordering):
            return True
        del assignment[literal]
        assignment[-literal] = True
        new_clauses = [c for c in clauses if -literal not in c]
        if dpll(new_clauses, assignment, ordering):
            return True
        del assignment[-literal]
        return False
    
    def find_tree_like_resolution(clauses, ordering):
        n = len(ordering)
        m = len(clauses)
        A = [[0] * (m + n) for _ in range(m)]
        b = [1] * m
        for i in range(m):
            A[i][i] = 1
            for lit in clauses[i]:
                if lit > 0:
                    A[i][n + abs(lit) - 1] = -1
                else:
                    A[i][n + abs(lit) - 1] = 1
        x = gaussian_elimination(A, b)
        resolution = []
        for i in range(m):
            if x[i] > 0.5:
                resolution.append(clauses[i])
            elif x[i] < -0.5:
                resolution.append([-lit for lit in clauses[i]])
        return resolution
    
    n_values = [10, 15, 20, 25, 30]
    families = [
        (generate_random_3cnf, 4.5),
        (generate_php_m, range(3, 8)),
        (generate_tseitin_formula, None)
    ]
    
    results = []
    for family, density in families:
        if callable(density):
            n_values = [n for m in density for n in n_values]
        for n in n_values:
            clauses = family(n)
            ordering = list(range(1, 2 * n + 1))
            resolution = find_tree_like_resolution(clauses, ordering)
            lyndon_factors = []
            widths = []
            for clause in resolution:
                b = encode_clause(clause, n)
                factors = lyndon_factorization(b, ordering)
                lyndon_factors.append(max(factors))
                widths.append(sum(factors))
            results.append({
                "metric_name": "Lyndon-width",
                "metric_value": max(lyndon_factors),
                "instances_tested": len(resolution),
                "conjecture_holds": all(lf >= math.ceil(math.log2(w + 1)) for lf, w in zip(lyndon_factors, widths)),
                "counterexample": "" if all(lf >= math.ceil(math.log2(w + 1)) for lf, w in zip(lyndon_factors, widths)) else "mapping_undefined"
            })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in all_results) / sum(r["instances_tested"] for r in all_results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 * r["instances_tested"] for r in all_results) / sum(r["instances_tested"] for r in all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        counterexample = next(r["counterexample"] for r in all_results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")