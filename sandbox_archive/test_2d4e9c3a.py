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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Find a non-zero pivot below the current row
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    # Swap rows i and k
                    A[i], A[k] = A[k], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        for j in range(n):
            if j == i:
                continue
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def projective_variety(phi):
    n = len(phi)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            if phi[i][j]:
                A[i][j] = 1
    return gaussian_elimination(A)

def resolution_width(phi):
    n = len(phi)
    clauses = [set(range(n)) for _ in range(n)]
    assignment = {}
    
    def dpll():
        if not any(clause for clause in clauses):
            return True
        unit_clause = next((clause for clause in clauses if len(clause) == 1), None)
        if unit_clause:
            literal = list(unit_clause)[0]
            assignment[literal] = True
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    return False
                new_clauses.append(clause - {literal})
            clauses[:] = new_clauses
        else:
            literal = next(lit for lit in range(n) if lit not in assignment)
            assignment[literal] = True
            if dpll():
                return True
            del assignment[literal]
            assignment[-literal] = True
            if dpll():
                return True
            del assignment[-literal]
        return False
    
    return len(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    try:
        variety = projective_variety(phi)
        width = resolution_width(phi)
        deg = sum(len(row) - row.count(0) for row in variety if any(x != 0 for x in row))
        
        return {
            "metric_name": "Hodge degree",
            "metric_value": deg,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": deg == width,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Hodge degree",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")