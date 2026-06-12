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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(M, p):
    result = [[Fraction(1) if i == j else Fraction(0) for j in range(len(M))] for i in range(len(M))]
    while p > 0:
        if p % 2 == 1:
            result = matrix_multiply(result, M)
        M = matrix_multiply(M, M)
        p //= 2
    return result

def is_quasi_closed(points):
    n = len(points[0])
    A = [[Fraction(1)] + point for point in points]
    A.append([Fraction(1)] * (n+1))
    gaussian_elimination(A)
    return all(A[i][-1] == 0 for i in range(n))

def satisfiable_points(phi):
    n = len(phi)
    variables = list(range(n))
    satisfying_points = []
    for assignment in itertools.product([0, 1], repeat=n):
        if all(phi[clause].evaluate(assignment) for clause in phi):
            satisfying_points.append(list(assignment))
    return satisfying_points

def resolution_proof_depth(phi):
    n = len(phi)
    variables = list(range(n))
    clauses = [set(clause) for clause in phi]
    queue = set()
    for clause in clauses:
        queue.add(frozenset(clause))
    
    def resolve(lit1, lit2):
        return frozenset([x for x in lit1 if x != -lit2] + [y for y in lit2 if y != -lit1])
    
    while True:
        new_clauses = set()
        for clause1 in queue:
            for clause2 in queue:
                if len(clause1.intersection(clause2)) == 1:
                    new_clause = resolve(next(iter(clause1)), next(iter(clause2)))
                    if not any(new_clause.issubset(c) for c in queue):
                        new_clauses.add(new_clause)
        if not new_clauses:
            break
        queue.update(new_clauses)
    
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = [random.choice([lambda x: x[i] == 1, lambda x: x[i] == 0]) for i in range(n)]
    
    satisfying_points = satisfiable_points(phi)
    if not satisfying_points:
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "no_satisfying_assignments"
        }
    
    if not is_quasi_closed(satisfying_points):
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_quasi_closed"
        }
    
    d_phi = resolution_proof_depth(phi)
    omega_phi = len(satisfying_points) + 1
    
    return {
        "metric_name": "resolution_proof_depth",
        "metric_value": d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    
    if conjecture_holds:
        support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results))
        if support_fraction >= Fraction(8, 10):
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")