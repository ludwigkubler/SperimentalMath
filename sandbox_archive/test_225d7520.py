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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        unique_clauses = set()
        for _ in range(10):  # Generate 10 instances per size
            clauses = random.sample(range(n), n)
            unique_clauses.update(clauses)
        
        p = random.choice([2, 3, 5, 7, 11])  # Prime number for modulo operation
        
        def clause_indicator_polynomial(clauses):
            poly = [0] * (n + 1)
            for c in clauses:
                poly[c] += 1
            return poly
        
        def modular_function_rank(poly, p):
            n = len(poly) - 1
            A = [[poly[j] ** i % p for i in range(n + 1)] for j in range(n + 1)]
            rank = gaussian_elimination(A)
            return rank
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                if A[i][i] == 0:
                    continue
                
                for j in range(i + 1, m):
                    factor = A[j][i] / A[i][i]
                    for k in range(n + 1):
                        A[j][k] -= factor * A[i][k]
            
            rank = sum(1 for row in A if any(row))
            return rank
        
        poly = clause_indicator_polynomial(list(unique_clauses))
        mfr_value = modular_function_rank(poly, p)
        
        results.append({
            "n": n,
            "unique_clauses": len(unique_clauses),
            "mfr_value": mfr_value
        })
    
    if not results:
        return {
            "metric_name": "mfr(I)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    mfr_values = [result["mfr_value"] for result in results]
    unique_clause_counts = [result["unique_clauses"] for result in results]
    
    if n_max < 16:
        return {
            "metric_name": "mfr(I)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    correlation = pearson_correlation(mfr_values, unique_clause_counts)
    
    return {
        "metric_name": "mfr(I)",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results if "metric_value" in r)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if "metric_value" in r))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")