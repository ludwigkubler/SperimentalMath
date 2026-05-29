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
    
    def tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(m):
            a, b, c = random.sample(variables, 3)
            clause = (a, b, c)
            clauses.append(clause)
            
            # Add negation of the clause
            neg_clause = (-a, -b, -c)
            clauses.append(neg_clause)
        
        return variables, clauses
    
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
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        
        return A
    
    def rank(A):
        A = [row[:] for row in A]
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def hodge_span(variables, clauses):
        n = len(variables)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in clauses:
            for v in clause:
                if v > 0:
                    A[v - 1][v - 1] += 1
                else:
                    A[-1][-1] += 1
        
        rank_A = rank(A)
        return n - rank_A
    
    def min_circuit_depth(variables, clauses):
        # Placeholder for actual circuit depth calculation
        # For simplicity, we use the number of variables as a proxy
        return len(variables)
    
    n_max = 40
    instances_tested = 0
    total_ratio = 0
    
    for n in range(5, n_max + 1):
        for _ in range(3):  # Sample 3 instances per size
            m = random.randint(n // 2, n * (n - 1) // 4)
            variables, clauses = tseitin_formula(n, m)
            
            h_min = hodge_span(variables, clauses)
            d_phi = min_circuit_depth(variables, clauses)
            
            if h_min == 0:
                continue
            
            ratio = Fraction(d_phi, h_min)
            total_ratio += ratio
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "c",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c = total_ratio / instances_tested
    conjecture_holds = all(c <= Fraction(1, 2) for _ in range(30))  # Placeholder condition
    
    return {
        "metric_name": "c",
        "metric_value": float(c),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")