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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def hodge_complexity(phi):
        n = len(phi)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if phi[i] == phi[j]:
                    A[i][j] = 1
                    A[j][i] = 1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def dpll_proof_tree_height(phi):
        n = len(phi)
        clauses = [set(map(int, clause.split())) for clause in phi]
        variables = set(abs(lit) for lit in sum(clauses, []))
        
        def solve(model):
            if not any(clause - model for clause in clauses):
                return 1
            var = next(var for var in variables if var not in model)
            pos, neg = {var}, {-var}
            return max(solve(model | pos), solve(model | neg)) + 1
        
        return solve(set())
    
    n_values = [5, 10, 15, 20, 30, 40]
    hdc_sum = 0
    h_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            phi = [' '.join(str(random.choice([-1, 1]) * random.randint(1, n)) for _ in range(n)) for _ in range(n)]
            hdc_value = hodge_complexity(phi)
            h_value = dpll_proof_tree_height(phi)
            
            if hdc_value == 0 or h_value == 0:
                continue
            
            hdc_sum += hdc_value
            h_sum += h_value
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "hdc_h_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    hdc_mean = hdc_sum / instances_tested
    h_mean = h_sum / instances_tested
    ratio_mean = hdc_mean / h_mean
    
    return {
        "metric_name": "hdc_h_ratio",
        "metric_value": ratio_mean,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= ratio_mean <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    hdc_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(hdc_values)/len(hdc_values):.2f} std={math.sqrt(sum((x - sum(hdc_values)/len(hdc_values))**2 for x in hdc_values) / len(hdc_values)):.2f} support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_out_of_bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")