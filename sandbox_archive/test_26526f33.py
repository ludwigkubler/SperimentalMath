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

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mult(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def matrix_inv(A):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    inv_det = mod_inverse(det, 2)
    if inv_det == -1:
        raise ValueError('Matrix is not invertible')
    return [[inv_det * (A[1][1] if i == j else -A[1][j]) for j in range(2)] for i in range(2)]

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError('Matrix is singular')
        for j in range(n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def frege_proof_depth(cnf):
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    variables = set.union(*clauses)
    assignment = {var: None for var in variables}
    
    def dpll(assignment, clauses):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = list(unit_clause)[0]
            assignment[var] = 1 if var > 0 else -1
            new_clauses = [c.difference({var}) for c in clauses if var not in c and -var not in c]
            return dpll(assignment, new_clauses)
        pure_literal = next((var for var in variables if (var in assignment or -var in assignment) == False), None)
        if pure_literal:
            assignment[pure_literal] = 1
            new_clauses = [c.difference({pure_literal}) for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(assignment, new_clauses)
        var = next(iter(variables))
        assignment[var] = 1
        if dpll(assignment, clauses):
            return True
        assignment[var] = -1
        return dpll(assignment, clauses)
    
    return len(cnf) if not dpll(assignment, clauses) else 0

def groupoid_representation(cnf):
    n = len(cnf)
    variables = set.union(*[set(clause) for clause in cnf])
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if (i+1) in cnf[j] and (j+1) not in cnf[i]:
                A[i][j] = 1
            elif (i+1) not in cnf[j] and (j+1) in cnf[i]:
                A[j][i] = 1
    return sum(sum(row) for row in A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            cnf = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
            frege_depth = frege_proof_depth(cnf)
            if frege_depth == 0:
                continue
            A_G = groupoid_representation(cnf)
            metric_values.append(A_G / frege_depth)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(0.5 <= value <= 1.5 for value in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_representation_dimension",
        "metric_value": mean_value,
        "instances_tested": instances_tested * len([5, 10, 15, 20, 30, 40]),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")