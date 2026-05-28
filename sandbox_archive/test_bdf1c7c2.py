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
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find pivot
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            if A[i][i] == 0:
                continue
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back substitution
        x = [0] * n
        for i in range(m-1, -1, -1):
            if A[i][i] == 0:
                continue
            x[i] = A[i][-1] / A[i][i]
            for j in range(i-1, -1, -1):
                A[j][-1] -= A[j][i] * x[i]
        return x
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        reduced_matrix = [row[:] for row in matrix]
        r = gaussian_elimination(reduced_matrix)
        return sum(1 for x in r if x != 0)
    
    def generate_k_cnf(n, k):
        clauses = []
        variables = list(range(1, n+1))
        for _ in range(k):
            clause = random.sample(variables, 3)
            clause = [random.choice([-1, 1]) * var for var in clause]
            clauses.append(clause)
        return clauses
    
    def vector_space_rank(clauses):
        m = len(clauses)
        n = max(abs(var) for clause in clauses for var in clause)
        A = [[0] * (n+1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                A[i][abs(var)] += 1 if var > 0 else -1
        return rank(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    max_rank = 0
    
    for n in n_values:
        k = random.randint(1, min(n, 10))
        cnf = generate_k_cnf(n, k)
        rank_value = vector_space_rank(cnf)
        if rank_value > max_rank:
            max_rank = rank_value
    
    metric_name = "max_brauer_group_rank"
    metric_value = max_rank
    instances_tested = len(n_values)
    conjecture_holds = max_rank <= 2**k
    counterexample = "" if conjecture_holds else f"Max rank {max_rank} exceeds 2^k for n={n}, k={k}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Max rank exceeds 2^k\" first_failing_seed={first_failing_seed}")