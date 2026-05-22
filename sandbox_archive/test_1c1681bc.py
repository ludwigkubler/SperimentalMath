# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        if matrix[i][i] == 0:
            return None  # Singular matrix
        for j in range(i + 1, rows):
            factor = -Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] += factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def is_independent(points):
    n = len(points[0])
    A = [[points[j][i] for i in range(n)] for j in range(len(points))]
    rank = gaussian_elimination(A)
    return rank == len(points)

def construct_affine_variety(clauses, num_vars):
    points = []
    for clause in clauses:
        point = [0] * num_vars
        for var in clause:
            if var > 0:
                point[var - 1] += 1
            else:
                point[-var - 1] -= 1
        points.append(point)
    return points

def resolution_length(clauses):
    stack = clauses[:]
    visited = set()
    while stack:
        clause = stack.pop()
        if len(clause) == 0:
            return 1
        literal = random.choice(clause)
        for other_clause in clauses:
            if -literal in other_clause:
                new_clause = [l for l in other_clause if l != -literal]
                if new_clause not in visited:
                    stack.append(new_clause)
                    visited.add(new_clause)
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    num_vars = n
    clauses = []
    for _ in range(n):
        clause = [random.randint(-num_vars, num_vars) for _ in range(3)]
        clauses.append(clause)
    
    variety_points = construct_affine_variety(clauses, num_vars)
    independent_points = [p for p in variety_points if is_independent([p] + variety_points)]
    geometric_defect = len(independent_points)
    
    proof_length = resolution_length(clauses)
    
    M = 2  # Example constant multiple
    conjecture_holds = proof_length <= M * geometric_defect
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Proof length {proof_length} exceeds M * geometric defect {M * geometric_defect}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")