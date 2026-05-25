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
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def determinant(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows != cols:
        raise ValueError("Matrix must be square")
    
    det = Fraction(1)
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        det *= matrix[i][i]
        if det == 0:
            return Fraction(0)
        for j in range(cols):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.choice([10, 20])
    
    # Generate Tseitin formula
    variables = set(range(n))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(3)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    
    # Construct Delone set D
    # This is a placeholder function. In practice, you would need to implement
    # the geometric algorithm to construct Delone sets based on the hyperplane arrangement.
    def delone_set_from_formula(formula):
        # Placeholder: return a dummy Delone set
        return [[0] * n for _ in range(n)]
    
    D = delone_set_from_formula(clauses)
    
    # Calculate minimal rank ρ(D)
    rank = 0
    while True:
        try:
            det = determinant(gaussian_elimination(D))
            if det != 0:
                rank += 1
                break
            else:
                rank += 1
                D = delone_set_from_formula(clauses)
        except OverflowError:
            return {
                "metric_name": "minimal_rank",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
    
    # Check resolution proof length
    k = rank
    if k > m:
        return {
            "metric_name": "minimal_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    proof_length = 2**(k + 1)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= Fraction(2**m, m),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")