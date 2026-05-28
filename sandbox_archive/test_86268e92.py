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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if all(abs(x) < 1e-9 for x in A[i]):
                continue
            rank += 1
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def tropicalize_matrix(A):
        m, n = len(A), len(A[0])
        T = [[float('inf')] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if A[i][j] != 0:
                    T[i][j] = -math.log(abs(A[i][j]))
        return T
    
    def generate_boolean_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        formula = []
        for _ in range(n):
            clause = random.sample(literals, 3)
            clause = ' & '.join(clause)
            formula.append(f'~{clause}')
        return ' | '.join(formula)
    
    def resolution_length(formula):
        # Simplified resolution length calculation
        return len(formula.split(' | '))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different formulas
            formula = generate_boolean_formula(n)
            length = resolution_length(formula)
            if length > n**2:  # Arbitrary upper bound to avoid trivial cases
                continue
            total_length += length
            instances_tested += 1
            
            # Convert formula to Lie algebra (simplified example)
            L = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            T_L = tropicalize_matrix(L)
            rank = matrix_rank(T_L)
            total_rank += rank
    
    if instances_tested == 0:
        return {
            "metric_name": "Average Minimal Rank",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid formulas generated"
        }
    
    average_rank = total_rank / instances_tested
    avg_length_per_instance = total_length / instances_tested
    
    return {
        "metric_name": "Average Minimal Rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": average_rank >= avg_length_per_instance**2,  # Simplified check
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_rank} std=nan support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "First failing seed"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)