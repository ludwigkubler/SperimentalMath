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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    return result

def gaussian_elimination(M, b):
    n = len(b)
    M_b = [row + [b[i]] for i, row in enumerate(M)]
    
    for i in range(n):
        if M_b[i][i] == 0:
            for j in range(i+1, n):
                if M_b[j][i] != 0:
                    M_b[i], M_b[j] = M_b[j], M_b[i]
                    break
            else:
                raise ValueError("No non-zero pivot found")
        
        for j in range(n):
            if i == j:
                continue
            factor = M_b[j][i] / M_b[i][i]
            for k in range(n+1):
                M_b[j][k] -= factor * M_b[i][k]
    
    x = [M_b[i][n] / M_b[i][i] for i in range(n)]
    return x

def rank(M):
    M_rref = gaussian_elimination(M, [0]*len(M))
    rref_rank = sum(1 for row in M_rref if any(row[j] != 0 for j in range(len(row)-1)))
    return rref_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances_tested = 0
    total_minimal_rank = 0
    counterexample = ""
    
    for n in n_values:
        instances_tested = 0
        minimal_rank_sum = 0
        
        for _ in range(5):  # Test 5 random inputs per size
            x = [random.randint(0, 1) for _ in range(n)]
            y = [random.randint(0, 1) for _ in range(n)]
            
            if x == y:
                continue
            
            instances_tested += 1
            total_instances_tested += 1
            
            # Construct matrix algebra over a skew field (simplified)
            M = [[x[i] * y[j] - y[i] * x[j] for j in range(n)] for i in range(n)]
            
            minimal_rank = rank(M)
            minimal_rank_sum += minimal_rank
            
            if minimal_rank < n and instances_tested == 1:
                counterexample = f"n={n}, x={x}, y={y}"
        
        if instances_tested > 0:
            avg_minimal_rank = Fraction(minimal_rank_sum, instances_tested)
            total_minimal_rank += avg_minimal_rank
    
    mean_metric_value = Fraction(total_minimal_rank, len(n_values))
    
    conjecture_holds = all(avg_minimal_rank >= n for avg_minimal_rank, n in zip([Fraction(x, y) for x, y in zip(total_minimal_rank.numerator, total_minimal_rank.denominator)], n_values))
    
    return {
        "metric_name": "Average Minimal Rank",
        "metric_value": mean_metric_value,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")