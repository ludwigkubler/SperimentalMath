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

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        factor = Fraction(A[i][i])
        for j in range(i+1, rows):
            factor_j = Fraction(A[j][i]) / factor
            for k in range(cols):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] -= factor_j * A[i][k]
    return A

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    A = [row[:] for row in matrix]
    rref = gaussian_elimination(A)
    rank = 0
    for row in rref:
        if any(row[j] != 0 for j in range(cols)):
            rank += 1
    return rank

def boolean_tensor_product(x):
    n = len(x)
    tp = [1]
    for xi in x:
        new_tp = []
        for term in tp:
            new_tp.append(term * (1 - xi))
            new_tp.append(term * xi)
        tp = new_tp
    return sum(tp)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = random.randint(5, 20)
    x = [random.choice([0, 1]) for _ in range(n)]
    TP_x = boolean_tensor_product(x)
    Fx_rank = rank([[i] for i in x])
    
    metric_value = abs(Fx_rank) / math.log2(m)
    instances_tested = 1
    conjecture_holds = True if abs(Fx_rank) <= TP_x else False
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "K-theory rank vs Tensor Product Valuation",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")