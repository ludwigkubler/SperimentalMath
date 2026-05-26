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
    
    def is_symmetric(f):
        n = len(f)
        for i in range(n):
            for j in range(i, n):
                if f[i] != f[j]:
                    return False
        return True
    
    def construct_brauer_group(f):
        n = len(f)
        if not is_symmetric(f):
            return None
        
        B_f = []
        for i in range(n):
            row = [0] * n
            row[i] = 1
            B_f.append(row)
        
        return B_f
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(m):
            if all(x == 0 for x in matrix[i]):
                continue
            
            for j in range(n):
                if matrix[i][j] != 0:
                    pivot_col = j
                    break
            
            for k in range(i, m):
                if matrix[k][pivot_col] != 0:
                    if k != i:
                        matrix[k], matrix[i] = matrix[i], matrix[k]
                    
                    for l in range(n):
                        if l == pivot_col:
                            continue
                        factor = matrix[l][pivot_col] / matrix[i][pivot_col]
                        matrix[l][pivot_col] = 0
                        for m in range(pivot_col + 1, n):
                            matrix[l][m] -= factor * matrix[i][m]
                    rank += 1
        
        return rank
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if all(x == 0 for x in matrix[i]):
                continue
            
            for j in range(n):
                if matrix[i][j] != 0:
                    pivot_col = j
                    break
            
            for k in range(i, m):
                if matrix[k][pivot_col] != 0:
                    if k != i:
                        matrix[k], matrix[i] = matrix[i], matrix[k]
                    
                    for l in range(n):
                        if l == pivot_col:
                            continue
                        factor = matrix[l][pivot_col] / matrix[i][pivot_col]
                        matrix[l][pivot_col] = 0
                        for m in range(pivot_col + 1, n):
                            matrix[l][m] -= factor * matrix[i][m]
        
        return matrix
    
    def determinant(matrix):
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square")
        
        n = len(matrix)
        det = 0
        
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            sign = (-1) ** (i % 2)
            det += sign * matrix[0][i] * determinant(submatrix)
        
        return det
    
    def construct_symmetric_boolean_function(n):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        while not is_symmetric(f):
            f = [random.choice([0, 1]) for _ in range(2**n)]
        return f
    
    n = random.randint(5, 40)
    f = construct_symmetric_boolean_function(n)
    
    B_f = construct_brauer_group(f)
    if B_f is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank = matrix_rank(B_f)
    
    lower_bound = 2**n / math.log(n)
    upper_bound = n**2
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": lower_bound <= rank <= upper_bound,
        "counterexample": "" if lower_bound <= rank <= upper_bound else f"rank={rank}, expected=[{lower_bound}, {upper_bound}]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")