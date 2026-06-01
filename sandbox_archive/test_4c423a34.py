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
            # Find the pivot row
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate non-pivot elements
            for j in range(m):
                if i != j:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        
        return A
    
    def lattice_points_covering(A, b):
        n = len(b)
        A_augmented = [row + [b[i]] for i, row in enumerate(A)]
        A_rref = gaussian_elimination(A_augmented)
        
        L = 0
        for row in A_rref:
            if any(row[j] != 0 for j in range(n)):
                L += 1
        
        return L
    
    def dpll_search_tree_diameter(n, m):
        # Simplified DPLL search tree diameter calculation (not accurate but serves as a placeholder)
        return n + m
    
    instances_tested = 0
    n_max = 0
    total_L = 0
    total_D = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n, 2*n)
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
            b = [random.randint(-10, 10) for _ in range(m)]
            
            L = lattice_points_covering(A, b)
            D = dpll_search_tree_diameter(n, m)
            
            total_L += L
            total_D += D
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_L = Fraction(total_L, instances_tested)
    mean_D = Fraction(total_D, instances_tested)
    correlation_coefficient = (mean_L * mean_D - mean_L * mean_D) / (math.sqrt(mean_L**2 * mean_D**2))
    
    conjecture_holds = 0.5 <= correlation_coefficient < 0.8
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient} is out of the acceptable range [0.5, 0.8)"
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_L = sum(r["metric_value"] for r in results) / len(results)
    mean_D = sum(r["instances_tested"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_L} std={math.sqrt(sum((r['metric_value'] - mean_L)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")