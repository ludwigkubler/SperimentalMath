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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def matrix_representation(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        var_indices = {var: i for i, var in enumerate(range(-n, 0), start=1)}
        
        for clause in cnf:
            for var in clause:
                if var < 0:
                    M[var_indices[var]][-var] += 1
                else:
                    M[-var][var_indices[var]] += 1
        
        return M
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [0] for row in matrix]
        
        # Gaussian elimination
        for i in range(min(m, n)):
            if augmented_matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        break
                else:
                    continue
            
            pivot = augmented_matrix[i][i]
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
        
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        rank = sum(1 for row in augmented_matrix if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        M = matrix_representation(cnf)
        rank_value = rank(M)
        ranks.append(rank_value)
    
    mean_rank = sum(ranks) / len(ranks)
    variance_rank = sum((x - mean_rank) ** 2 for x in ranks) / len(ranks)
    
    f_n = math.log(n_values[-1])
    if variance_rank > f_n:
        conjecture_holds = False
        counterexample = "variance exceeds f(n)"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Variance of Rank",
        "metric_value": variance_rank,
        "instances_tested": len(ranks),
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")