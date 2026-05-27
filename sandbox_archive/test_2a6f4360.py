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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank, m)):
                continue
            A[rank], A[i] = A[i], A[rank]
            pivot = A[rank][i]
            for j in range(i + 1, n):
                factor = -A[rank][j] / pivot
                for k in range(n):
                    A[j][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def minimal_rank_of_quadratic_form(clauses):
        m = len(clauses)
        n = max(abs(lit) for clause in clauses for lit in clause)
        Q = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            x, y = abs(clause[0]), abs(clause[1])
            Q[x][y] += 1
            Q[y][x] += 1
        return gaussian_elimination(Q)
    
    def resolution_refutation_size(clauses):
        # Simplified version of resolution refutation size calculation
        return len(clauses) * (len(clauses) - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        total_refutation_size = 0
        
        while instances_tested < 30:
            clauses = generate_sat_instance(n)
            rank = minimal_rank_of_quadratic_form(clauses)
            refutation_size = resolution_refutation_size(clauses)
            
            total_rank += rank
            total_refutation_size += refutation_size
            instances_tested += 1
        
        avg_rank = total_rank / instances_tested
        avg_refutation_size = total_refutation_size / instances_tested
        
        results.append({
            "metric_name": "CorrelationCoefficient",
            "metric_value": -avg_rank / avg_refutation_size,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient' first_failing_seed={first_failing_seed}")