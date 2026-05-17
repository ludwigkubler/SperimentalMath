# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def lit(l, assignment):
    var = abs(l)
    if var not in assignment:
        return None
    if l > 0:
        return assignment[var]
    else:
        return not assignment[var]

def backtrack(assignment, clauses):
    if len(assignment) == len(clauses):
        return True
    var = len(assignment) + 1
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        if all(any(lit(l, new_assignment) for l in clause) for clause in clauses):
            if backtrack(new_assignment, clauses):
                return True
    return False

def is_satisfiable(F, n):
    return backtrack({}, F)

def generate_3cnf(n, alpha):
    m = int(alpha * n)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            if random.random() < 0.5:
                clause[i] = -clause[i]
        clauses.append(clause)
    return clauses

def generate_tseitin(n):
    variables = list(range(1, n + 1))
    edges = list(itertools.combinations(variables, 2))
    random.shuffle(edges)
    clauses = []
    for u, v in edges[:n]:
        x = random.choice([u, -u])
        y = random.choice([v, -v])
        clauses.append([x, y, -(u + v)])
    return clauses

def matrix_mult(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_rank(M, tol=1e-9):
    n = len(M)
    rank = 0
    for i in range(n):
        if max(abs(M[i][j]) for j in range(n)) < tol:
            continue
        rank += 1
        for j in range(i + 1, n):
            factor = Fraction(M[j][i], M[i][i]) if M[i][i] != 0 else 0
            for k in range(i, n):
                M[j][k] -= factor * M[i][k]
    return rank

def compute_hessian(F, n, u):
    H = [[0 for _ in range(n)] for _ in range(n)]
    for clause in F:
        a, b, c = clause
        for i in range(n):
            for j in range(n):
                term = 1
                for l in clause:
                    var = abs(l)
                    if var == i + 1 or var == j + 1:
                        if l > 0:
                            term *= u[var - 1]
                        else:
                            term *= (1 - u[var - 1])
                    else:
                        if l > 0:
                            term *= u[var - 1]
                        else:
                            term *= (1 - u[var - 1])
                H[i][j] += term
    return H

def compute_mu_H(F, n):
    u = [random.random() for _ in range(n)]
    H = compute_hessian(F, n, u)
    r_F = matrix_rank(H)
    return math.floor(math.log2(1 + r_F))

def resolution_width(F, max_width=8):
    clauses = [set(clause) for clause in F]
    for width in range(1, max_width + 1):
        new_clauses = []
        for clause1, clause2 in itertools.combinations(clauses, 2):
            if len(clause1.intersection(clause2)) == width - 1:
                resolvent = clause1.symmetric_difference(clause2)
                if len(resolvent) == width:
                    new_clauses.append(resolvent)
        if not new_clauses:
            return width
        clauses.extend(new_clauses)
    return max_width

def run_trial(seed):
    random.seed(seed)
    n = random.choice([10, 15, 20, 25, 30, 35, 40])
    alpha = random.choice([5, 6, 8])
    is_tseitin = random.random() < 0.5

    if is_tseitin:
        F = generate_tseitin(n)
    else:
        F = generate_3cnf(n, alpha)

    if not is_satisfiable(F, n):
        mu_H = compute_mu_H(F, n)
        w_star = resolution_width(F)
        conjecture_holds = mu_H <= w_star
        counterexample = f"mu_H={mu_H} > w*={w_star}" if not conjecture_holds else ""
        return {
            "metric_name": "mu_H",
            "metric_value": mu_H,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "mu_H",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["instances_tested"] > 0:
            metric_values.append(result["metric_value"])
            conjecture_holds.append(result["conjecture_holds"])

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_unsat_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)

    if all(conjecture_holds):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for seed in seeds:
            result = run_trial(seed)
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={seed}")
                sys.exit(0)