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

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(A_augmented[k][i]))
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        for j in range(i + 1, n):
            factor = A_augmented[j][i] / A_augmented[i][i]
            A_augmented[j] = [A_augmented[j][k] - factor * A_augmented[i][k] for k in range(n + 1)]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_augmented[i][-1] - sum(A_augmented[i][j] * x[j] for j in range(i + 1, n))) / A_augmented[i][i]
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def characteristic_polynomial(A):
    n = len(A)
    if n == 1:
        return [A[0][0], -1]
    elif n == 2:
        a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
        return [a * d - b * c, -(a + d), 1]
    else:
        det_A = 0
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det_A += A[0][j] * ((-1) ** j) * characteristic_polynomial(submatrix)[0]
        return [det_A, -sum(A[i][i] for i in range(n)), 1]

def tropical_divisors(poly):
    divisors = set()
    for i in range(1, len(poly)):
        if poly[i] != 0:
            divisors.add(i)
    return divisors

def dpll(clauses, assignment={}):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        var = unit_clause[0]
        if var in assignment and assignment[var] != unit_clause[0]:
            return False
        assignment[var] = unit_clause[0]
        clauses = [c for c in clauses if var not in c or (var, -var) in zip(c, c)]
    pure_literal = next((v for v in assignment if all(v not in clause and -v not in clause for clause in clauses)), None)
    if pure_literal is not None:
        assignment[pure_literal] = 1
        clauses = [c for c in clauses if pure_literal not in c or (-pure_literal, pure_literal) in zip(c, c)]
    if not any(clause for clause in clauses):
        return True
    var = next((v for v in range(1, len(clauses[0]) + 1)), None)
    new_assignment = assignment.copy()
    new_assignment[var] = 1
    if dpll(clauses, new_assignment):
        return True
    new_assignment[var] = -1
    if dpll(clauses, new_assignment):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_height = 0
    total_divisors = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            variables = list(range(1, n + 1))
            clauses = []
            for _ in range(n):
                clause = [random.choice(variables) if random.random() < 0.8 else -random.choice(variables) for _ in range(random.randint(1, n))]
                clauses.append(clause)
            A = [[0] * (n + 1) for _ in range(n)]
            for i, clause in enumerate(clauses):
                for var in clause:
                    if var > 0:
                        A[i][var - 1] += 1
                    else:
                        A[i][-1] -= 1
            poly = characteristic_polynomial(A)
            divisors = tropical_divisors(poly)
            height = dpll(clauses)
            total_height += height
            total_divisors += len(divisors)
            instances_tested += 1
            n_max = max(n_max, n)

    mean_height = total_height / instances_tested
    std_dev = math.sqrt(sum((height - mean_height) ** 2 for height in range(total_height)) / instances_tested)
    correlation_coefficient = (total_height * sum(divisors) - instances_tested * mean_height * sum(divisors)) / (instances_tested * std_dev * sum(divisors))
    if correlation_coefficient < 0.8 or abs(mean_height - sum(divisors)) > 3:
        conjecture_holds = False
        counterexample = "correlation_coefficient=<{}> mean_height_diff=<{}>".format(correlation_coefficient, abs(mean_height - sum(divisors)))

    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": mean_height,
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
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_height = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_height) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_height, std_dev, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample={} first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")