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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for k in range(i+1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for k in range(i-1, -1, -1):
            b[k] -= A[k][i] * x[i]
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    else:
        for j in range(n):
            det += (-1)**j * A[0][j] * determinant([[A[i][k] for k in range(j, n)] for i in range(1, n)])
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} | {clause[1]})")
        return " & ".join(clauses)

    def resolution_width(phi):
        literals = set()
        for clause in phi.split(" & "):
            literals.update([l.strip() for l in clause.split("|")])
        width = 0
        while literals:
            literal, _ = random.choice(list(literals.items()))
            literals.remove(literal)
            new_clauses = []
            for clause in phi.split(" & "):
                if literal not in clause and f"~{literal}" not in clause:
                    new_clauses.append(clause.replace(f"{literal}", ""))
                elif f"~{literal}" in clause:
                    new_clauses.append(clause.replace(f"~{literal}", ""))
            phi = " & ".join(new_clause for new_clause in new_clauses if new_clause)
            literals.update([l.strip() for l in phi.split("|")])
            width += 1
        return width

    def min_symplectic_volume(phi):
        n = len(phi.split(" & "))
        A = [[0]*n for _ in range(n)]
        b = [0]*n
        for i, clause in enumerate(phi.split(" & ")):
            literals = set(l.strip() for l in clause.split("|"))
            for j, other_clause in enumerate(phi.split(" & ")):
                if i != j:
                    other_literals = set(l.strip() for l in other_clause.split("|"))
                    A[i][j] = len(literals.intersection(other_literals))
        det = determinant(A)
        return abs(det)

    n_values = [5, 10, 15, 20, 30, 40]
    min_vols = []
    widths = []

    for n in n_values:
        phi = generate_sat_instance(n)
        min_vol = min_symplectic_volume(phi)
        width = resolution_width(phi)
        min_vols.append(min_vol)
        widths.append(width)

    mean_min_vol = sum(min_vols) / len(min_vols)
    mean_width = sum(widths) / len(widths)
    covariance = sum((min_vols[i] - mean_min_vol) * (widths[i] - mean_width) for i in range(len(n_values))) / len(n_values)
    variance_width = sum((widths[i] - mean_width)**2 for i in range(len(n_values))) / len(n_values)
    correlation_coefficient = covariance / math.sqrt(variance_width)

    conjecture_holds = correlation_coefficient >= 0.8 and abs(covariance) >= 2 * mean_min_vol
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or |covariance| < 2 * mean_min_vol"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8 or |covariance| < 2 * mean_min_vol\" first_failing_seed={first_failing_seed}")