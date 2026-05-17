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
    trace = 0
    for i in range(n):
        trace += m[i][i]
    return trace

def burau_generator(n, k, exponent):
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        if i == k:
            m[i][i] = 1
        elif i == k + 1:
            m[i][i] = 1
            m[i][k] = exponent
        else:
            m[i][i] = 1
    return m

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = []
        while len(clause) < 3:
            var = random.choice(variables)
            sign = random.choice([-1, 1])
            literal = sign * var
            if literal not in clause:
                clause.append(literal)
        clauses.append(clause)
    return clauses

def is_unsat(clauses, n):
    assignments = []
    for _ in range(2 ** n):
        assignment = [(-1) ** ((_ >> i) & 1) for i in range(n)]
        assignments.append(assignment)

    for assignment in assignments:
        satisfied = False
        for clause in clauses:
            for literal in clause:
                var = abs(literal)
                if (literal > 0 and assignment[var - 1] == 1) or (literal < 0 and assignment[var - 1] == -1):
                    satisfied = True
                    break
            if satisfied:
                break
        if not satisfied:
            return True
    return False

def dpll_backtrack_count(clauses, n):
    def backtrack(assignment, clauses):
        if not clauses:
            return 0
        for clause in clauses:
            if len(clause) == 1:
                literal = clause[0]
                var = abs(literal)
                if var in assignment and assignment[var] != (1 if literal > 0 else -1):
                    return float('inf')
                assignment[var] = 1 if literal > 0 else -1
                return backtrack(assignment, [c for c in clauses if c != clause])
        for clause in clauses:
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment[var] = 1 if literal > 0 else -1
                    count = backtrack(new_assignment, [c for c in clauses if c != clause])
                    if count != float('inf'):
                        return count + 1
        return float('inf')

    return backtrack({}, clauses)

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16]
    alpha = 6
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = alpha * n
        clauses = generate_3cnf(n, m, seed)
        if not is_unsat(clauses, n):
            continue

        instances_tested += 1
        beta = []
        for clause in sorted(clauses, key=lambda c: [abs(l) for l in c]):
            l1, l2, l3 = sorted(clause, key=lambda l: abs(l))
            k1 = abs(l1) - 1
            k2 = abs(l2) - 1
            if k1 >= n - 1 or k2 >= n - 1:
                continue
            exponent1 = (1 if l1 > 0 else -1) * (1 if l2 > 0 else -1)
            exponent2 = (1 if l2 > 0 else -1) * (1 if l3 > 0 else -1)
            beta.append((k1, exponent1))
            beta.append((k2, exponent2))

        M = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for k, exponent in beta:
            M = matrix_mult(M, burau_generator(n, k, exponent))

        omega = abs(n - matrix_trace(M))
        t = dpll_backtrack_count(clauses, n)

        if 4 * (t ** 2 + 1) < omega:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, omega={omega}, t={t}"

    return {
        "metric_name": "omega",
        "metric_value": omega if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    support_fraction = 0
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["instances_tested"] > 0:
            metric_values.append(result["metric_value"])
            if result["conjecture_holds"]:
                support_fraction += 1
            else:
                if first_failing_seed is None:
                    first_failing_seed = seed

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction /= len(metric_values)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")