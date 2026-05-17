# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from fractions import Fraction

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
    trace = 0
    for i in range(n):
        trace += m[i][i]
    return trace

def burau_generator(n, k, exponent):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        if i == k:
            matrix[i][i] = 1
        elif i == k + 1:
            matrix[i][i] = -1
            matrix[i][k] = exponent
        else:
            matrix[i][i] = 1
    return matrix

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            if random.random() < 0.5:
                clause.append(-var)
            else:
                clause.append(var)
        clauses.append(clause)
    return clauses

def is_unsat(clauses, n):
    assignments = [None] * (n + 1)
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if assignments[var] is None:
                assignments[var] = lit > 0
            elif (assignments[var] and lit < 0) or (not assignments[var] and lit > 0):
                return False
    return True

def lex_dpll(clauses, n):
    assignments = [None] * (n + 1)
    backtracks = 0

    def backtrack(level):
        nonlocal backtracks
        if level == n + 1:
            return True
        var = level
        for val in [True, False]:
            assignments[var] = val
            if is_satisfiable(clauses, assignments):
                if backtrack(level + 1):
                    return True
            assignments[var] = None
            backtracks += 1
        return False

    def is_satisfiable(clauses, assignments):
        for clause in clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if assignments[var] is not None:
                    if (assignments[var] and lit > 0) or (not assignments[var] and lit < 0):
                        satisfied = True
                        break
            if not satisfied:
                return False
        return True

    backtrack(1)
    return backtracks

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = 6 * n
        clauses = generate_3cnf(n, m, seed)
        if not is_unsat(clauses, n):
            continue

        instances_tested += 1
        beta = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for clause in sorted(clauses):
            l1, l2, l3 = sorted(clause, key=lambda x: abs(x))
            k1 = abs(l1) - 1
            k2 = abs(l2) - 1
            if k1 >= n - 1 or k2 >= n - 1:
                continue
            exponent1 = (1 if l1 > 0 else -1) * (1 if l2 > 0 else -1)
            exponent2 = (1 if l2 > 0 else -1) * (1 if l3 > 0 else -1)
            g1 = burau_generator(n, k1, exponent1)
            g2 = burau_generator(n, k2, exponent2)
            beta = matrix_mult(beta, matrix_mult(g1, g2))

        omega = abs(n - matrix_trace(beta))
        t = lex_dpll(clauses, n)

        if 4 * (t ** 2 + 1) < omega:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, omega={omega}, t={t}"

        metric_values.append(omega)

    if not metric_values:
        return {
            "metric_name": "omega",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    metric_value = sum(metric_values) / len(metric_values)

    return {
        "metric_name": "omega",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    metric_values = []
    conjecture_holds_all = True
    first_counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            if not first_counterexample:
                first_counterexample = result["counterexample"]
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{first_counterexample}" first_failing_seed={seeds[results.index(next(r for r in results if not r["conjecture_holds"]))]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')