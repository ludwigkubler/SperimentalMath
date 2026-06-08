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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(boolean_func, n):
        literals = list(range(-n, 0))
        clauses = []
        
        # Convert boolean function to CNF
        for i in range(2**n):
            binary_rep = format(i, f'0{n}b')
            clause = [literals[int(bit)] if bit == '1' else -literals[int(bit)] for bit in binary_rep]
            clauses.append(clause)
        
        # Add Tseitin variables
        tseitin_vars = list(range(n + 1, n + len(clauses) + 1))
        for i, clause in enumerate(clauses):
            literals_clause = [tseitin_vars[i]] + [-l for l in clause]
            clauses.append(literals_clause)
        
        # Add clauses for OR gates
        for i in range(n):
            literals_or = [literals[i], -tseitin_vars[n + i]]
            clauses.append(literals_or)
        
        return clauses
    
    def minimal_diophantine_exponent(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        
        for i, clause in enumerate(clauses):
            for l in clause:
                if l > 0:
                    A[i][l - 1] += 1
                else:
                    A[i][-1] -= 1
        
        # Gaussian elimination to find the rank of A
        def gaussian_elimination(A, b):
            n = len(A)
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                b[i], b[max_row] = b[max_row], b[i]
                
                pivot = A[i][i]
                for j in range(i, n + 1):
                    A[i][j] /= pivot
                b[i] /= pivot
                
                for j in range(n):
                    if j != i:
                        factor = A[j][i]
                        for k in range(i, n + 1):
                            A[j][k] -= factor * A[i][k]
                        b[j] -= factor * b[i]
            
            rank = sum(1 for row in A if any(row))
            return rank
        
        return gaussian_elimination(A, b)
    
    def communication_complexity_rank(clauses):
        n = len(clauses)
        rank = 0
        seen = set()
        
        for clause in clauses:
            clause_set = set(abs(l) for l in clause)
            if not clause_set.intersection(seen):
                rank += 1
                seen.update(clause_set)
        
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        boolean_func = generate_boolean_function(n)
        tseitin_clauses = tseitin_formula(boolean_func, n)
        
        diophantine_exponent = minimal_diophantine_exponent(tseitin_clauses)
        communication_rank = communication_complexity_rank(tseitin_clauses)
        
        results.append((diophantine_exponent, communication_rank))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x = [r[0] for r in results]
    y = [r[1] for r in results]
    correlation = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.5 else f"correlation={correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] is None), None)
        print(f"RESULT: INCONCLUSIVE reason=missing_data first_failing_seed={first_failing_seed}")