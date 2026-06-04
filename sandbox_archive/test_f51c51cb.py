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
    
    def generate_formula(depth):
        if depth == 1:
            return random.choice(['A', 'B', 'C'])
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(depth - 1)
            right = generate_formula(depth - 1)
            return f"({left} {op} {right})"
    
    def incidence_matrix(formula):
        if formula.isalpha():
            return [[0]]
        
        op, left, right = formula[1:-2].split()
        left_matrix = incidence_matrix(left)
        right_matrix = incidence_matrix(right)
        
        n_left = len(left_matrix)
        n_right = len(right_matrix)
        
        result = [[0] * (n_left + n_right) for _ in range(n_left + n_right)]
        
        for i in range(n_left):
            for j in range(n_right):
                if op == '&':
                    result[i][j + n_left] = 1
                elif op == '|':
                    result[j][i + n_right] = 1
        
        return result
    
    def gramian_matrix(matrix):
        n = len(matrix)
        G = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    G[i][j] += matrix[i][k] * matrix[j][k]
        
        return G
    
    def min_symplectic_form_rank(gramian):
        n = len(gramian)
        rank = 0
        
        for i in range(n):
            pivot_found = False
            for j in range(i, n):
                if gramian[j][i] != 0:
                    # Swap rows to make the pivot non-zero
                    gramian[i], gramian[j] = gramian[j], gramian[i]
                    pivot_found = True
                    break
            
            if not pivot_found:
                continue
            
            rank += 1
            for j in range(i + 1, n):
                factor = Fraction(gramian[j][i], gramian[i][i])
                for k in range(n):
                    gramian[j][k] -= factor * gramian[i][k]
        
        return rank
    
    def frege_proof_depth(formula):
        if formula.isalpha():
            return 1
        else:
            op, left, right = formula[1:-2].split()
            return 1 + max(frege_proof_depth(left), frege_proof_depth(right))
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in depths:
        formula = generate_formula(depth)
        incidence = incidence_matrix(formula)
        gramian = gramian_matrix(incidence)
        sfr = min_symplectic_form_rank(gramian)
        d = frege_proof_depth(formula)
        
        if d == 0:
            continue
        
        results.append((sfr, d))
    
    if not results:
        return {
            "metric_name": "symplectic_form_rank_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    sfr_values, d_values = zip(*results)
    correlation_coefficient = sum(sfr * d for sfr, d in results) / (sum(sfr**2 for sfr in sfr_values) * sum(d**2 for d in d_values))**0.5
    
    return {
        "metric_name": "symplectic_form_rank_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(depths),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(1 <= sfr / d <= 2 for sfr, d in results),
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")