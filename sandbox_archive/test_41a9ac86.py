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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for k in range(i+1, n):
                factor = A[k][i] / A[i][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = A[i][-1]
            for k in range(i+1, n):
                x[i] -= A[i][k] * x[k]
            x[i] /= A[i][i]
        
        return x
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
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
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for c in range(n):
                det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det
    
    def hodge_rank(A):
        n = len(A)
        if n == 0:
            return 0
        elif n == 1:
            return int(A[0][0] != 0)
        
        # Perform Gaussian elimination to find the rank
        A_copy = [row[:] for row in A]
        rank = gaussian_elimination(A_copy)
        
        # Count non-zero rows
        rank_count = sum(1 for row in rank if any(x != 0 for x in row))
        return rank_count
    
    def lidb(resolution_proof):
        n = len(resolution_proof)
        lidb_value = 0
        for clause in resolution_proof:
            lidb_value += len(clause)
        return lidb_value
    
    def generate_formula(n):
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(10):  # Generate 10 random clauses
            clause = random.sample(variables, k=random.randint(1, n))
            clause.append("~" + random.choice(clause))  # Add a negation
            clauses.append(clause)
        return clauses
    
    def resolution_proof(formula):
        proof = []
        for clause in formula:
            if any(var.startswith("~") for var in clause):
                continue
            proof.append(clause)
        return proof
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        proof = resolution_proof(formula)
        
        lidb_value = lidb(proof)
        hodge_rank_value = hodge_rank([[random.randint(0, 1) for _ in range(n)] for _ in range(n)])
        
        results.append({
            "n": n,
            "lidb": lidb_value,
            "hodge_rank": hodge_rank_value
        })
    
    if not all(result["hodge_rank"] != 0 for result in results):
        return {
            "metric_name": "LIDB vs Hodge Rank",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "Hodge rank computation failed"
        }
    
    lidb_values = [result["lidb"] for result in results]
    hodge_rank_values = [result["hodge_rank"] for result in results]
    
    mean_lidb = sum(lidb_values) / len(lidb_values)
    mean_hodge_rank = sum(hodge_rank_values) / len(hodge_rank_values)
    
    correlation_coefficient = (sum((lidb_values[i] - mean_lidb) * (hodge_rank_values[i] - mean_hodge_rank) for i in range(len(lidb_values))) /
                               math.sqrt(sum((lidb_values[i] - mean_lidb) ** 2 for i in range(len(lidb_values)))) *
                               math.sqrt(sum((hodge_rank_values[i] - mean_hodge_rank) ** 2 for i in range(len(hodge_rank_values)))))
    
    return {
        "metric_name": "LIDB vs Hodge Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(correlation_coefficient >= 0.5 for _ in range(len(results))),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")