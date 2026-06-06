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
        cnf = []
        for _ in range(10):  # Generate 10 clauses with n variables each
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def matrix_representation(cnf):
        n = len(cnf[0])
        M = [[0] * (2*n) for _ in range(2*n)]
        
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    i, j = lit - 1, n + lit - 1
                else:
                    i, j = -lit - 1, -lit - 1
                
                M[i][j] = 1
                M[j][i] = 1
        
        return M
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        
        # Gaussian elimination
        for i in range(m):
            max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            if augmented_matrix[i][i] == 0:
                return float('inf')  # Singular matrix
            
            for j in range(i + 1, m):
                factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        rank = sum(1 for row in augmented_matrix if any(row))
        return rank
    
    def variance(ranks, n):
        mean = sum(ranks) / len(ranks)
        var = sum((x - mean) ** 2 for x in ranks) / len(ranks)
        return var
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        M = matrix_representation(cnf)
        r = rank(M)
        if r == float('inf'):
            return {
                "metric_name": "variance",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "singular_matrix"
            }
        ranks.append(r)
    
    if len(ranks) < 30:
        return {
            "metric_name": "variance",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    var = variance(ranks, n)
    f_n = math.log(len(n_values))
    
    return {
        "metric_name": "variance",
        "metric_value": var,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(var - f_n) < 0.1 * f_n,  # Threshold for Θ(log(n))
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_var = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_var = math.sqrt(sum((r["metric_value"] - mean_var) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_var} std={std_var} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_var} std={std_var} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"variance_out_of_bound\" first_failing_seed={r['seed']}")
                break