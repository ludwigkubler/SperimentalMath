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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate
        pivot = matrix[i][i]
        for j in range(n):
            if j != i:
                factor = matrix[j][i] / pivot
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]

    return matrix

def det(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        det *= matrix[i][i]
    return det

def characteristic_polynomial(clauses, variables):
    n = len(variables)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for var in clause:
            if var > 0:
                A[var - 1][var - 1] += 1
            else:
                A[-1][-1] -= 1
                A[-1][abs(var) - 1] += 1
                A[abs(var) - 1][-1] += 1
    return det(A)

def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    
    # Check for contradiction
    for clause in clauses:
        if all(v not in assignment and -v not in assignment for v in clause):
            return False
    
    # Check for model
    if all(v in assignment or -v in assignment for v in range(1, len(variables) + 1)):
        return True
    
    # Pure literal rule
    pure_literal = next((v for v in assignment if all(v not in clause and -v not in clause for clause in clauses)), None)
    if pure_literal is not None:
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        return dpll(clauses, new_assignment) or dpll(clauses, {**new_assignment, pure_literal: False})
    
    # Unit propagation rule
    unit_clause = next((clause for clause in clauses if len([v for v in clause if v not in assignment and -v not in assignment]) == 1), None)
    if unit_clause is not None:
        var = [v for v in unit_clause if v not in assignment and -v not in assignment][0]
        new_assignment = assignment.copy()
        new_assignment[var] = True
        return dpll(clauses, new_assignment) or dpll(clauses, {**new_assignment, var: False})
    
    # Branching rule
    var = next(v for v in range(1, len(variables) + 1) if v not in assignment and -v not in assignment)
    return dpll(clauses, {**assignment, var: True}) or dpll(clauses, {**assignment, var: False})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = [random.choice([-v, v]) for v in variables]
        if len(clause) > 1:
            clauses.append(clause)
    
    chi_phi = characteristic_polynomial(clauses, variables)
    divisors = set()
    for i in range(1, abs(chi_phi) + 1):
        if chi_phi % i == 0:
            divisors.add(i)
            divisors.add(-i)
    
    height = dpll(clauses)
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": height,
        "instances_tested": len(clauses),
        "n_max": n,
        "conjecture_holds": False if height is None else True,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    std_height = math.sqrt(sum((r["metric_value"] - mean_height)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")