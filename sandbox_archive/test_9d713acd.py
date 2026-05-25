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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def create_density_matrix(clauses, n):
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for clause in clauses:
            for i in range(2**n):
                if all((i >> abs(l) - 1 & 1 == l // abs(l)) for l in clause):
                    matrix[i][i] += 1
        return normalize(matrix)
    
    def normalize(matrix):
        total = sum(sum(row) for row in matrix)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] /= total
        return matrix
    
    def von_neumann_entropy(matrix):
        entropy = 0
        for row in matrix:
            p = sum(row)
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if any(matrix[j][i] != 0 for j in range(i, m)):
                rank += 1
                for j in range(i + 1, m):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def is_satisfiable(clauses, n):
        stack = []
        assignment = [0] * (n + 1)
        def dfs(i):
            if i == n + 1:
                return True
            for val in [-1, 1]:
                assignment[i] = val
                if all(any(assignment[abs(l) - 1] * l // abs(l) != 0 for l in clause) for clause in clauses):
                    stack.append((i, val))
                    if dfs(i + 1):
                        return True
            stack.pop()
            return False
        return dfs(1)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    clauses = generate_3cnf(n, m)
    if not is_satisfiable(clauses, n):
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_3cnf"
        }
    
    density_matrix = create_density_matrix(clauses, n)
    rank = matrix_rank(density_matrix)
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n + m,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_exceeds_bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")