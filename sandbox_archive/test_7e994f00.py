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
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        pivot = A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A_augmented[j][i]
                for k in range(i, n+1):
                    A_augmented[j][k] -= factor * A_augmented[i][k]
    return [row[-1] for row in A_augmented]

def matrix_multiply(A, B):
    m, p = len(A), len(B[0])
    n = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = Fraction(1, 1)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -Fraction(1, 1)
    return det

def run_single_instance():
    n = random.randint(5, 40)
    clauses = [random.sample(range(n), random.randint(1, n)) for _ in range(random.randint(1, n))]
    diophantine_terms = []
    for clause in clauses:
        term = [0] * n
        for lit in clause:
            if lit < 0:
                term[-lit-1] -= 1
            else:
                term[lit-1] += 1
        diophantine_terms.append(term)
    
    A = [[sum(diophantine_terms[i][j] * diophantine_terms[j][k] for j in range(n)) for k in range(n)] for i in range(n)]
    b = [sum(diophantine_terms[i][j] for j in range(n)) for i in range(n)]
    
    rank = len(gaussian_elimination(A, b))
    degree = max(sum(abs(lit) for lit in term if lit != 0) for term in diophantine_terms)
    return degree, rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    degrees = []
    ranks = []
    
    for _ in range(30):
        degree, rank = run_single_instance()
        degrees.append(degree)
        ranks.append(rank)
    
    if not degrees or not ranks:
        return {
            "metric_name": "degree_rank_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_instance"
        }
    
    mean_degree = sum(degrees) / len(degrees)
    mean_rank = sum(ranks) / len(ranks)
    variance_rank = sum((r - mean_rank)**2 for r in ranks) / len(ranks)
    correlation_coefficient = sum((d - mean_degree) * (r - mean_rank) for d, r in zip(degrees, ranks)) / (len(degrees) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "degree_rank_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(degrees),
        "n_max": max(len(diophantine_terms) for _ in range(30)),
        "conjecture_holds": abs(correlation_coefficient) <= 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")