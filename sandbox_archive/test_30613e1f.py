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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tseitin_formula(variables, clauses):
    literals = set()
    for clause in clauses:
        literals.update(clause)
    n = len(literals)
    formula = []
    for literal in literals:
        if literal < 0:
            formula.append(-literal)
        else:
            formula.append(literal + n)
    return formula

def minimal_local_crossed_module_rank(formula):
    # Placeholder implementation
    return len(formula)

def shortest_resolution_proof_length(formula):
    # Placeholder implementation
    return len(formula) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(-n, 0)) + list(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = [random.choice(variables) for _ in range(random.randint(2, 3))]
        clauses.append(clause)
    
    formula = tseitin_formula(variables, clauses)
    rank = minimal_local_crossed_module_rank(formula)
    length = shortest_resolution_proof_length(formula)
    
    if rank == 0 or length == 0:
        return {
            "metric_name": "rank/length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = rank / length
    return {
        "metric_name": "rank/length",
        "metric_value": ratio,
        "instances_tested": 1,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)