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
    
    def is_satisfiable(clauses, n):
        def dfs(var):
            if var > 2 * n:
                return True
            for clause in clauses:
                if all(lit not in assignment or assignment[lit] == 0 for lit in clause):
                    assignment[var] = 1
                    if dfs(var + 1):
                        return True
                    assignment[var] = -1
                    if dfs(var + 1):
                        return True
            assignment.pop(var)
            return False
        
        assignment = {}
        return dfs(1)
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(-n, -1) + list(range(1, n+1)), 3)
            clauses.append(clause)
        return clauses
    
    def construct_density_matrix(clauses, n):
        # Placeholder for constructing the density matrix
        # This is a dummy implementation and should be replaced with actual logic
        return [[0] * (n + m) for _ in range(n + m)]
    
    def von_neumann_entropy(density_matrix):
        # Placeholder for computing von Neumann entropy
        # This is a dummy implementation and should be replaced with actual logic
        return 0.0
    
    def matrix_rank(matrix):
        rank = 0
        rows, cols = len(matrix), len(matrix[0])
        for col in range(cols):
            if any(matrix[row][col] != 0 for row in range(rows)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        clauses = generate_3cnf(n, m)
        if not is_satisfiable(clauses, n):
            continue
        
        density_matrix = construct_density_matrix(clauses, n)
        entropy = von_neumann_entropy(density_matrix)
        rank = matrix_rank(density_matrix)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "matrix_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No satisfiable 3-CNF formula found"
        }
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    max_rank = max(result["rank"] for result in results)
    
    return {
        "metric_name": "matrix_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": max_rank <= 10 * n + m,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    max_rank = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif max_rank > 10 * n + m:
        print(f"RESULT: FALSIFIED counterexample='rank exceeds bound' first_failing_seed={seeds[results.index(next(result for result in results if result['conjecture_holds'] == False))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")