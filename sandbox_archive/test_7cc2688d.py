# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def f(x):
        return [random.randint(0, 1) for _ in range(k)]
    
    def IND_2(y):
        return [(y >> i) & 3 for i in range(k)]
    
    def subword_complexity(s: str, n: int) -> int:
        seen = set()
        for i in range(len(s) - n + 1):
            window = s[i:i+n]
            if window not in seen:
                seen.add(window)
        return len(seen)
    
    k_values = [2, 3, 4]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for k in k_values:
        for _ in range(100):
            f = [f(x) for x in range(2**k)]
            M = [[f[i][j] if (i & (1 << j)) else 0 for j in range(k)] for i in range(2**k)]
            
            rank_M = matrix_rank(M, tolerance=1e-8)
            rows = [''.join(str(bit) for bit in row) for row in M]
            p_r_x_values = [subword_complexity(row, k) for row in rows]
            s_f = max(p_r_x_values)
            
            if rank_M < s_f:
                conjecture_holds = False
                counterexample = f"First failing (f,x): {f}, {rows[0]}, {k}"
                break
            
            total_metric_value += rank_M / s_f
            instances_tested += 1
    
    return {
        "metric_name": "tightness_ratio",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def matrix_rank(matrix, tolerance=1e-8):
    m = len(matrix)
    n = len(matrix[0])
    rank = 0
    
    for i in range(n):
        if all(abs(matrix[j][i]) < tolerance for j in range(m)):
            continue
        
        pivot_row = next(j for j in range(i, m) if abs(matrix[j][i]) > tolerance)
        
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        for j in range(m):
            if i == j:
                continue
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
        
        rank += 1
    
    return rank

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    total_metric_value = sum(result["metric_value"] for result in seeds if "metric_value" in result)
    instances_tested = sum(result["instances_tested"] for result in seeds if "instances_tested" in result)
    support_fraction = sum(1 for result in seeds if result["conjecture_holds"]) / len(seeds)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in seeds):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0 support_fraction=1")
    elif any("counterexample" in result for result in seeds):
        counterexample = next(result["counterexample"] for result in seeds if "counterexample" in result)
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")