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

def lit(l, x):
    if l.startswith('¬'):
        return 1 - x[int(l[1:]) - 1]
    else:
        return x[int(l) - 1]

def construct_hessian(F, n):
    hessian = [[0 for _ in range(n)] for _ in range(n)]
    for clause in F:
        l1, l2, l3 = clause
        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                term = 0
                for c in range(n):
                    if c == a or c == b:
                        continue
                    term += lit(l1, [0]*n)[c] * lit(l2, [0]*n)[c] * lit(l3, [0]*n)[c]
                hessian[a][b] += term
    return hessian

def matrix_rank(matrix, tol=1e-9):
    n = len(matrix)
    rank = 0
    for row in matrix:
        if any(abs(x) > tol for x in row):
            rank += 1
    return rank

def is_satisfiable(F, n):
    def backtrack(assignment, clauses):
        if not clauses:
            return True
        for clause in clauses:
            if all(not lit(l, assignment) for l in clause):
                return False
        for var in range(1, n + 1):
            if var not in assignment:
                new_assignment = assignment.copy()
                new_assignment[var] = 1
                if backtrack(new_assignment, clauses):
                    return True
                new_assignment[var] = 0
                if backtrack(new_assignment, clauses):
                    return True
                return False
        return False
    return backtrack({}, F)

def generate_random_3cnf(n, alpha):
    F = []
    for _ in range(int(alpha * n)):
        clause = []
        for _ in range(3):
            var = random.randint(1, n)
            neg = random.choice([True, False])
            if neg:
                clause.append(f'¬{var}')
            else:
                clause.append(str(var))
        F.append(clause)
    return F

def generate_tseitin_formula(n):
    F = []
    edges = list(itertools.combinations(range(1, n + 1), 2))
    random.shuffle(edges)
    for i, (u, v) in enumerate(edges[:n]):
        F.append([f'¬{u}', f'¬{v}', str(i + n + 1)])
        F.append([str(u), str(i + n + 1)])
        F.append([str(v), str(i + n + 1)])
    return F

def resolution_width(F, n, max_width=8):
    clauses = [set(clause) for clause in F]
    for width in range(1, max_width + 1):
        new_clauses = []
        for clause1, clause2 in itertools.combinations(clauses, 2):
            if len(clause1.intersection(clause2)) == width - 1:
                resolvent = clause1.symmetric_difference(clause2)
                if len(resolvent) <= width:
                    new_clauses.append(resolvent)
        clauses.extend(new_clauses)
        if any(len(clause) == 0 for clause in clauses):
            return width
    return max_width + 1

def run_trial(seed):
    random.seed(seed)
    n = random.choice([10, 15, 20, 25, 30, 35, 40])
    alpha = random.choice([5, 6, 8])
    F = generate_random_3cnf(n, alpha)
    if not is_satisfiable(F, n):
        hessian = construct_hessian(F, n)
        u = [random.random() for _ in range(n)]
        hessian_u = [[sum(hessian[i][j] * u[k] for k in range(n)) for j in range(n)] for i in range(n)]
        r_F = matrix_rank(hessian_u)
        mu_H = math.floor(math.log2(1 + r_F))
        w_star = resolution_width(F, n)
        if mu_H > w_star:
            return {
                "metric_name": "mu_H(F) - w*(F)",
                "metric_value": mu_H - w_star,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"mu_H(F)={mu_H} > w*(F)={w_star}"
            }
        else:
            return {
                "metric_name": "mu_H(F) - w*(F)",
                "metric_value": mu_H - w_star,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
    else:
        return {
            "metric_name": "mu_H(F) - w*(F)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [result["metric_value"] for result in results if result["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_unsat_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={first_failing_seed}")