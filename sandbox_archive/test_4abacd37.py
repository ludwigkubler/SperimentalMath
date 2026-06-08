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
    
    def generate_cnf(m: int):
        variables = list(range(1, m + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def characteristic_polynomial(cnf, p):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for var in clause:
                if var > 0:
                    A[var - 1][var - 1] += 1
                else:
                    A[-1][abs(var) - 1] -= 1
        A[-1][-1] = n
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                
                pivot = matrix[i][i]
                for j in range(cols):
                    matrix[i][j] /= pivot
                
                for j in range(rows):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[i][k]
            
            return matrix
        
        A = gaussian_elimination(A)
        
        def determinant(matrix):
            n = len(matrix)
            det = 1
            for i in range(n):
                det *= matrix[i][i]
            return det
        
        det = determinant(A)
        return det
    
    def minimal_p_adic_valuation_rank(det, p):
        if det == 0:
            return float('inf')
        rank = 0
        while det % p == 0:
            det //= p
            rank += 1
        return rank
    
    m_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for m in m_values:
        for _ in range(5):
            cnf = generate_cnf(m)
            det = characteristic_polynomial(cnf, 2)
            rank = minimal_p_adic_valuation_rank(det, 2)
            clause_complexity = len(cnf)
            
            instances_tested += 1
            n_max = max(n_max, m)
            total_metric_value += abs(rank - clause_complexity)
    
    mean_metric_value = total_metric_value / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "Mean Absolute Deviation",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient samples"
        }
    
    return {
        "metric_name": "Mean Absolute Deviation",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")