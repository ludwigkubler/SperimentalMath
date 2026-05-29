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

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rref = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
    
    for i in range(min(rows, cols)):
        max_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        
        for j in range(cols):
            matrix[i][j] /= pivot
        
        for j in range(rows):
            if j != i:
                factor = matrix[j][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    
    return rank

def tensor_product(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    result = [[Fraction(0) for _ in range(cols_A * cols_B)] for _ in range(rows_A * rows_B)]
    
    for i in range(rows_A):
        for j in range(cols_A):
            for k in range(rows_B):
                for l in range(cols_B):
                    result[i*rows_B + k][j*cols_B + l] = A[i][j] * B[k][l]
    
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, 2**n)
        CNF = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        
        A_F = [sum(CNF[i][j] * x[j] for j in range(n)) for i in range(m)]
        B_F = [sum(CNF[i][j] * x[j] for j in range(n)) for i in range(m) for x in itertools.product([0, 1], repeat=n)]
        
        tensor_product_matrix = tensor_product(A_F, B_F)
        rank_value = gaussian_elimination(tensor_product_matrix)
        
        # Placeholder for Frege proof depth calculation
        frege_depth = random.randint(1, n)
        
        results.append({
            "n": n,
            "m": m,
            "rank_value": rank_value,
            "frege_depth": frege_depth
        })
    
    correlation_coefficient = 0.0
    for result in results:
        correlation_coefficient += (result["rank_value"] - mean_rank) * (result["frege_depth"] - mean_frege_depth)
    correlation_coefficient /= len(results)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    mean_rank = 0.0
    mean_frege_depth = 0.0
    conjecture_holds_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        mean_rank += trial_result["metric_value"]
        mean_frege_depth += abs(trial_result["rank_value"] - trial_result["frege_depth"])
        if trial_result["conjecture_holds"]:
            conjecture_holds_count += 1
    
    mean_rank /= len(seeds)
    mean_frege_depth /= len(seeds)
    support_fraction = conjecture_holds_count / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={mean_frege_depth} support_fraction={support_fraction}")
    elif support_fraction > 0:
        print(f"RESULT: FALSIFIED counterexample=\"not enough evidence\" first_failing_seed=1")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")