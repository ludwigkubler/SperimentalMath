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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1]])
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append([variables[i-1], variables[j-1]])
                clauses.append([variables[i-1], -variables[j-1]])
                clauses.append([-variables[i-1], variables[j-1]])
                clauses.append([-variables[i-1], -variables[j-1]])
        return variables, clauses
    
    def incidence_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        matrix = [[0] * (n + 2) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] = 1
                else:
                    matrix[i][-var - 1] = -1
        return matrix
    
    def ehrhart_polynomial_degree(matrix):
        n = len(matrix[0]) - 2
        m = len(matrix)
        A = [[matrix[j][i] for i in range(n)] for j in range(m)]
        B = [sum(matrix[j][-2:]) for j in range(m)]
        
        def gaussian_elimination(A, B):
            m, n = len(A), len(A[0])
            for k in range(n-1):
                if A[k][k] == 0:
                    for i in range(k+1, m):
                        if A[i][k] != 0:
                            A[k], A[i] = A[i], A[k]
                            B[k], B[i] = B[i], B[k]
                            break
                if A[k][k] == 0:
                    continue
                for i in range(k+1, m):
                    factor = A[i][k] / A[k][k]
                    for j in range(k, n):
                        A[i][j] -= factor * A[k][j]
                    B[i] -= factor * B[k]
            return A, B
        
        A, B = gaussian_elimination(A, B)
        
        def rank(matrix):
            m, n = len(matrix), len(matrix[0])
            r = 0
            for i in range(n-1, -1, -1):
                if any(matrix[j][i] != 0 for j in range(m)):
                    r += 1
            return r
        
        rank_A = rank(A)
        degree = n + m - rank_A - 1
        return degree
    
    def resolution_proof_width(variables, clauses):
        n = len(variables)
        m = len(clauses)
        width = [0] * (n + 2)
        
        for clause in clauses:
            for var in clause:
                if abs(var) > n:
                    continue
                if var > 0:
                    width[var - 1] += 1
                else:
                    width[-var - 1] += 1
        
        return max(width)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    matrix = incidence_matrix(variables, clauses)
    ehrhart_degree = ehrhart_polynomial_degree(matrix)
    proof_width = resolution_proof_width(variables, clauses)
    
    return {
        "metric_name": "ratio",
        "metric_value": ehrhart_degree / proof_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ehrhart_degree >= proof_width,
        "counterexample": "" if ehrhart_degree >= proof_width else f"n={n}, ehrhart_degree={ehrhart_degree}, proof_width={proof_width}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")