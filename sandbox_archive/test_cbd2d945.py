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
        if depth == 0:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_formula(depth - 1)
            right = generate_formula(depth - 1)
            return f"({left} {op} {right})"
    
    def incidence_matrix(formula):
        if formula == "True":
            return [[0]]
        elif formula == "False":
            return []
        
        op, left, right = formula.split()
        left_incidence = incidence_matrix(left)
        right_incidence = incidence_matrix(right)
        
        n_left = len(left_incidence)
        n_right = len(right_incidence)
        
        if op == 'AND':
            result = [[0] * (n_left + n_right) for _ in range(n_left)]
            for i in range(n_left):
                for j in range(n_right):
                    result[i][j] = 1
            return result
        elif op == 'OR':
            result = [[0] * (n_left + n_right) for _ in range(n_left + n_right)]
            for i in range(n_left):
                result[i][:n_left] = left_incidence[i]
            for j in range(n_right):
                result[n_left + j][n_left:] = right_incidence[j]
            return result
    
    def gramian_matrix(incidence):
        if not incidence:
            return []
        
        n = len(incidence)
        G = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i, n):
                sum_product = 0
                for k in range(len(incidence[0])):
                    sum_product += incidence[i][k] * incidence[j][k]
                G[i][j] = sum_product
                G[j][i] = sum_product
        
        return G
    
    def min_symplectic_form_rank(G):
        if not G:
            return 0
        
        n = len(G)
        rank = 0
        
        for i in range(n):
            pivot_row = next((j for j in range(i, n) if G[j][i] != 0), None)
            if pivot_row is None:
                continue
            rank += 1
            
            # Swap rows to put the pivot row at the current position
            G[i], G[pivot_row] = G[pivot_row], G[i]
            
            # Eliminate entries below the pivot
            for j in range(i + 1, n):
                factor = -G[j][i] / G[i][i]
                for k in range(n):
                    G[j][k] += factor * G[i][k]
        
        return rank
    
    def frege_proof_depth(formula):
        if formula == "True" or formula == "False":
            return 0
        else:
            op, left, right = formula.split()
            return 1 + max(frege_proof_depth(left), frege_proof_depth(right))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        incidence = incidence_matrix(formula)
        G = gramian_matrix(incidence)
        sfr = min_symplectic_form_rank(G)
        d = frege_proof_depth(formula)
        
        if sfr == 0 or d == 0:
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
    
    sfr_values = [r[0] for r in results]
    d_values = [r[1] for r in results]
    
    mean_sfr = sum(sfr_values) / len(sfr_values)
    mean_d = sum(d_values) / len(d_values)
    
    correlation_coefficient = sum((sfr - mean_sfr) * (d - mean_d) for sfr, d in results) / (len(results) * math.sqrt(sum((sfr - mean_sfr) ** 2 for sfr in sfr_values)) * math.sqrt(sum((d - mean_d) ** 2 for d in d_values)))
    
    return {
        "metric_name": "symplectic_form_rank_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and all(0.5 <= sfr / d <= 2 for sfr, d in results),
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.7\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")