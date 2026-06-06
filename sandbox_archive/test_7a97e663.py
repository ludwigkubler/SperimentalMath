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
    
    def generate_cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def indicator_polynomial(clauses, n):
        indicator = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            x, y = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                indicator[x][y] += 1
                indicator[y][x] += 1
            elif clause[0] < 0 and clause[1] < 0:
                indicator[-x][-y] += 1
                indicator[-y][-x] += 1
        return indicator
    
    def grothendieck_witt_class(indicator):
        n = len(indicator) - 1
        det = determinant(indicator)
        return math.sqrt(det)
    
    def adjacency_matrix(clauses, n):
        adj = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            x, y = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                adj[x][y] += 1
                adj[y][x] += 1
            elif clause[0] < 0 and clause[1] < 0:
                adj[-x][-y] += 1
                adj[-y][-x] += 1
        return adj
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def min_eigenvalue(matrix):
        n = len(matrix)
        eigenvalues = []
        for k in range(n):
            identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            A_k = matrix
            for _ in range(k):
                A_k = matrix_multiplication(A_k, A_k)
            lambda_k = sum(matrix[i][i] for i in range(n)) / n
            eigenvalues.append(lambda_k)
        return min(eigenvalues)
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        n = random.randint(2, min(m + 5, 30))
        clauses = generate_cnf(m, n)
        indicator = indicator_polynomial(clauses, n)
        gwc = grothendieck_witt_class(indicator)
        adj_matrix = adjacency_matrix(clauses, n)
        mev = min_eigenvalue(adj_matrix)
        
        if mev == 0:
            continue
        
        ratio = gwc / (math.sqrt(m) * math.sqrt(mev))
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "Grothendieck-Witt Class / sqrt(m) * sqrt(min_eigenvalue)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(results) / len(results)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Grothendieck-Witt Class / sqrt(m) * sqrt(min_eigenvalue)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": all(ratio >= 0.8 for ratio in results) and std_ratio <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    supported_trials = [r for r in results if r["conjecture_holds"]]
    support_fraction = len(supported_trials) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results):.2f} std={std_ratio:.2f} support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)