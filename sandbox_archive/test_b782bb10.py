# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_mult(a, b):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_trace(m):
    n = len(m)
    return sum(m[i][i] for i in range(n))

def burau_generator(k, n):
    matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    if k < n - 1:
        matrix[k][k] = 2
        matrix[k][k + 1] = -1
        matrix[k + 1][k] = -1
    return matrix

def compute_omega(clauses, n):
    beta = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for clause in sorted(clauses):
        literals = sorted(clause, key=lambda x: abs(x))
        if len(literals) == 3:
            l1, l2, l3 = literals
            k1 = abs(l1) - 1
            k2 = abs(l2) - 1
            s1 = 1 if l1 > 0 else -1
            s2 = 1 if l2 > 0 else -1
            s3 = 1 if l3 > 0 else -1
            if k1 < n - 1:
                beta = matrix_mult(burau_generator(k1, n), beta)
                if s1 * s2 == -1:
                    beta = matrix_mult(burau_generator(k1, n), beta)
            if k2 < n - 1:
                beta = matrix_mult(burau_generator(k2, n), beta)
                if s2 * s3 == -1:
                    beta = matrix_mult(burau_generator(k2, n), beta)
    trace = matrix_trace(beta)
    return abs(n - trace)

def is_unsat(clauses, n):
    assignment = {}
    queue = []
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                assignment[var] = None
    for var in assignment:
        if assignment[var] is None:
            queue.append((var, True))
            queue.append((var, False))
    while queue:
        var, val = queue.pop(0)
        if var in assignment and assignment[var] is not None and assignment[var] != val:
            return False
        assignment[var] = val
        for clause in clauses:
            if any(abs(lit) == var and (lit > 0) == val for lit in clause):
                continue
            unsatisfied = [lit for lit in clause if abs(lit) not in assignment or assignment[abs(lit)] != (lit > 0)]
            if not unsatisfied:
                return False
            if len(unsatisfied) == 1:
                lit = unsatisfied[0]
                new_var = abs(lit)
                new_val = lit > 0
                if new_var in assignment and assignment[new_var] is not None and assignment[new_var] != new_val:
                    return False
                if new_var not in assignment or assignment[new_var] is None:
                    queue.append((new_var, new_val))
    return True

def dpll_backtrack_count(clauses, n):
    def backtrack(assignment, clauses):
        if not clauses:
            return 0
        for clause in clauses:
            if all(abs(lit) in assignment and assignment[abs(lit)] != (lit > 0) for lit in clause):
                return 0
        for var in range(1, n + 1):
            if var not in assignment:
                for val in [True, False]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = val
                    new_clauses = [c for c in clauses if not any(abs(lit) == var and assignment[abs(lit)] != (lit > 0) for lit in c)]
                    count = backtrack(new_assignment, new_clauses)
                    if count != 0:
                        return count + 1
                return 0
        return 0
    return backtrack({}, clauses)

def generate_3cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            clause.add(sign * var)
        clauses.append(list(clause))
    return clauses

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    m = 6 * n
    clauses = generate_3cnf(n, m)
    if not is_unsat(clauses, n):
        return {
            "metric_name": "omega",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    omega = compute_omega(clauses, n)
    t = dpll_backtrack_count(clauses, n)
    conjecture_holds = 4 * (t ** 2 + 1) >= omega
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, omega={omega}, t={t}"
    return {
        "metric_name": "omega",
        "metric_value": omega,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results if r["metric_value"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")