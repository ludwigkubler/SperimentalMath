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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{variables[i-1]}'
            clauses.append(clause)
        return variables, clauses
    
    def construct_quiver_representation(variables, clauses):
        n = len(variables)
        quiver = [[0] * (n + len(clauses)) for _ in range(n + len(clauses))]
        for i in range(n):
            quiver[i][i] = 1
        for clause in clauses:
            ci = variables.index(clause) + n
            for var in clause.split():
                ai = variables.index(var)
                quiver[n+ai][ci] = 1
                quiver[ci][n+ai] = 1
        return quiver
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def compute_local_cohomology_rank(quiver):
        m, n = len(quiver), len(quiver[0])
        rank = 0
        for i in range(m):
            if quiver[i][i] != 1:
                continue
            rank += 1
            for j in range(n):
                if j != i and quiver[j][i] == 1:
                    for k in range(n):
                        quiver[j][k] -= quiver[i][k]
        return rank
    
    def resolution_proof_length(variables, clauses):
        proof_length = len(clauses)
        for clause in clauses:
            proof_length += len(clause.split())
        return proof_length
    
    variables, clauses = generate_tseitin_formula(10)  # Start with n=10
    quiver_representation = construct_quiver_representation(variables, clauses)
    if quiver_representation is None:
        return {
            "metric_name": "Local Cohomology Rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    local_cohomology_rank = compute_local_cohomology_rank(quiver_representation)
    proof_length = resolution_proof_length(variables, clauses)
    
    return {
        "metric_name": "Local Cohomology Rank",
        "metric_value": local_cohomology_rank,
        "instances_tested": 1,
        "conjecture_holds": proof_length >= 2**local_cohomology_rank and local_cohomology_rank <= math.log(len(variables), 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")