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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        cnf.append(clause)
    return cnf

def construct_groupoid(cnf):
    groupoid = {}
    for lit in range(-n, n + 1):
        if lit != 0:
            groupoid[lit] = []
    for clause in cnf:
        for lit in clause:
            groupoid[lit].append(abs(lit))
    return groupoid

def compute_adj_matrix(groupoid):
    adj_matrix = [[0] * len(groupoid) for _ in range(len(groupoid))]
    for lit, neighbors in groupoid.items():
        for neighbor in neighbors:
            i = list(groupoid.keys()).index(lit)
            j = list(groupoid.keys()).index(neighbor)
            adj_matrix[i][j] = 1
    return adj_matrix

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def compute_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(rows):
        if any(matrix[i][j] != 0 for j in range(cols)):
            rank += 1
    return rank

def compute_min_homrank(groupoid):
    adj_matrix = compute_adj_matrix(groupoid)
    reduced_matrix = gaussian_elimination(adj_matrix)
    min_homrank = compute_rank(reduced_matrix)
    return min_homrank

def sat_complexity(cnf):
    # Simplified DPLL solver for clause satisfiability complexity
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            lit = unit_clauses[0]
            new_assignment = assignment[:]
            new_assignment[lit] = True
            if dpll([c for c in clauses if lit not in c], new_assignment):
                return True
            new_assignment[lit] = False
            if dpll([c for c in clauses if -lit not in c], new_assignment):
                return True
        pure_lits = [l for l in range(1, n + 1) if (l in assignment and not -l in assignment) or (-l in assignment and not l in assignment)]
        if pure_lits:
            lit = pure_lits[0]
            new_assignment = assignment[:]
            new_assignment[lit] = True
            if dpll(clauses, new_assignment):
                return True
            new_assignment[lit] = False
            if dpll(clauses, new_assignment):
                return True
        return False

    complexity = 0
    for _ in range(10):  # Simplified sampling
        assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
        if not dpll(cnf, assignment):
            complexity += 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    groupoid = construct_groupoid(cnf)
    min_homrank = compute_min_homrank(groupoid)
    sat_complexity_val = sat_complexity(cnf)
    correlation_coefficient = (min_homrank - 1) / (sat_complexity_val + 1)  # Simplified linear correlation
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 10,  # Simplified sampling
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")