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
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([f'~{variables[i-1]}', variables[j-1]])
                clauses.append([f'~{variables[j-1]}', variables[i-1]])
        return variables, clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                raise ValueError("Matrix is singular")
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def compute_symmetry_invariant(variables, clauses):
        n = len(variables)
        G = [[0] * n for _ in range(n)]
        for clause in clauses:
            if len(clause) == 1:
                var = clause[0]
                i = int(var[1:]) - 1
                G[i][i] = 1
            elif len(clause) == 2:
                var1, var2 = clause[0], clause[1]
                i = int(var1[1:]) - 1
                j = int(var2[1:]) - 1
                G[i][j] = G[j][i] = 1
        return sum(sum(row) for row in G)
    
    def resolution_proof_complexity(clauses):
        m = len(clauses)
        A = [[0] * (m+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(i, m):
                if clauses[i][0] == f'~{clauses[j][0]}':
                    A[i][j] = A[j][i] = 1
        rank = gaussian_elimination(A)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        invariant = compute_symmetry_invariant(variables, clauses)
        proof_complexity = resolution_proof_complexity(clauses)
        results.append({
            "n": n,
            "invariant": invariant,
            "proof_complexity": proof_complexity
        })
    
    mean_complexity = sum(result["proof_complexity"] for result in results) / len(results)
    std_complexity = math.sqrt(sum((result["proof_complexity"] - mean_complexity) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["proof_complexity"] >= 2**(10 * n_values[0]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution Proof Complexity",
        "metric_value": mean_complexity,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_complexity = sum(result["metric_value"] for result in results) / len(results)
    std_complexity = math.sqrt(sum((result["metric_value"] - mean_complexity) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")