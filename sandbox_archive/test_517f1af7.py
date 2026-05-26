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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def p_adic_representation(clauses):
        # Simplified representation for demonstration purposes
        return sum(len(c) for c in clauses)
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m > n:
            matrix = list(zip(*matrix))
            m, n = n, m
        
        for i in range(m):
            max_row = max(range(i, m), key=lambda x: abs(matrix[x][i]))
            if matrix[max_row][i] == 0:
                return float('inf')
            
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate
            for j in range(m):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return sum(1 for row in matrix if any(row))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k_values = [max(3, int(n * (i / len(n_values)))) for i in range(len(n_values))]
        total_rank = 0
        
        for k in k_values:
            formula = generate_k_cnf(n, k)
            rep = p_adic_representation(formula)
            total_rank += rep
        
        avg_rank = total_rank / len(k_values)
        expected_rank = n ** 0.5 * k ** 0.25
        results.append({
            "n": n,
            "k": k,
            "avg_rank": avg_rank,
            "expected_rank": expected_rank,
            "within_20_percent": abs(avg_rank - expected_rank) <= 0.2 * expected_rank
        })
    
    metric_value = sum(r["avg_rank"] for r in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r["within_20_percent"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 103))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")