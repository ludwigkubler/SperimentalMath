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
    
    def generate_polynomial(n):
        coefficients = [random.choice([-1, 1]) for _ in range(n + 1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def is_parity_function(poly, n):
        for x in range(2**n):
            if evaluate_polynomial(poly, x) != sum(int(bit) % 2 for bit in bin(x)[2:].zfill(n)):
                return False
        return True
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            
            if pivot_row == -1:
                continue
            
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            
            for row in range(rows):
                if row != rank and matrix[row][col] != 0:
                    factor = matrix[row][col] / matrix[rank][col]
                    for j in range(cols):
                        matrix[row][j] -= factor * matrix[rank][j]
            
            rank += 1
        
        return rank
    
    def min_rank(poly, n):
        x_values = [x for x in range(2**n)]
        y_values = [evaluate_polynomial(poly, x) for x in x_values]
        
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == 0:
                    matrix[i][j] = sum(x**(j-1) for x in x_values)
                else:
                    matrix[i][j] = sum(y_values[k] * (x_values[k]**(i-1)) for k in range(2**n))
        
        return gaussian_elimination(matrix)
    
    n = random.randint(5, 40)
    poly = generate_polynomial(n)
    if not is_parity_function(poly, n):
        return {
            "metric_name": "min_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_parity_function"
        }
    
    rank = min_rank(poly, n)
    expected_rank = 2**n / (math.log(n) ** 2)
    if rank < 0.5 * expected_rank:
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank<{0.5*expected_rank}"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" not in r or r["counterexample"] == "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_parity_function\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")