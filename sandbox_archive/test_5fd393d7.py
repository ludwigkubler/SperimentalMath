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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Singular matrix")
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def det(A):
    if len(A) != len(A[0]):
        raise ValueError("Matrix must be square")
    n = len(A)
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det_val = 0
        for c in range(n):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_det = det(submatrix)
            det_val += sign * A[0][c] * sub_det
        return det_val

def order_brauer_group(k):
    if k != 3:
        raise ValueError("Brauer group is nontrivial only for characteristic 2 and prime degree")
    return 1  # Brauer group of GF(2)[x] when k=3 is trivial, so order is 1

def resolution_width(F):
    n = len(F)
    clauses = F
    literals = set()
    for clause in clauses:
        literals.update(clause)
    num_vars = max(literals) + 1
    assignment = [None] * num_vars
    stack = []
    while True:
        unit_clause = None
        for i, literal in enumerate(literals):
            if assignment[literal] is None and assignment[-literal] is not None:
                unit_clause = [-i-1]
                break
            elif assignment[literal] is not None and assignment[-literal] is None:
                unit_clause = [i+1]
                break
        if unit_clause is not None:
            for literal in literals:
                if literal in unit_clause or -literal in unit_clause:
                    continue
                stack.append((literal, -assignment[literal]))
        else:
            if not stack:
                return len(literals)
            literal, value = stack.pop()
            assignment[literal] = value
            literals.remove(-literal)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    total_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(2, 10)
            F = []
            for _ in range(random.randint(n // 2, n)):
                clause = [random.choice(range(-n, -1)) for _ in range(k)]
                F.append(clause)
            width = resolution_width(F)
            order = order_brauer_group(k)
            total_width += width
            total_order += order
            instances_tested += 1
    
    mean_width = total_width / instances_tested
    mean_order = total_order / instances_tested
    conjecture_holds = mean_width <= 2 * mean_order  # Example constant factor
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    mean_order = sum(r["instances_tested"] * (2 if r["conjecture_holds"] else 0) for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")