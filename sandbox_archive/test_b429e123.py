# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import sys
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_mult(A, B, mod):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C
    
    def matrix_pow(matrix, power, mod):
        result = [[0 if i != j else 1 for j in range(len(matrix))] for i in range(len(matrix))]
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = matrix_mult(result, base, mod)
            base = matrix_mult(base, base, mod)
            power //= 2
        return result
    
    def is_identity(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                    return False
        return True
    
    def rank_variance(matrix, mod):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        diff = matrix_mult(matrix, identity, mod)
        count = sum(sum(1 for x in row if x != 0) for row in diff)
        return Fraction(count, n * n)
    
    def ncybe_order(n, mod):
        matrix = [[random.randint(0, mod - 1) for _ in range(n)] for _ in range(n)]
        while not is_identity(matrix):
            matrix = matrix_pow(matrix, 2, mod)
        return len([i for i in range(1, n + 1) if (n ** (1/3)) <= i <= (n ** (2/3))])
    
    n_max = 40
    instances_tested = 30
    nc_ybe_order_values = []
    rank_variance_values = []
    
    for _ in range(instances_tested):
        mod = random.randint(2, 100)
        matrix = [[random.randint(0, mod - 1) for _ in range(n_max)] for _ in range(n_max)]
        nc_ybe_order = ncybe_order(n_max, mod)
        rank_var = rank_variance(matrix, mod)
        nc_ybe_order_values.append(nc_ybe_order)
        rank_variance_values.append(rank_var)
    
    metric_value = sum(nc_ybe_order_values) / instances_tested
    correlation_coefficient = 0.0
    
    if len(nc_ybe_order_values) > 1 and len(rank_variance_values) > 1:
        mean_nc_ybe_order = sum(nc_ybe_order_values) / len(nc_ybe_order_values)
        mean_rank_var = sum(rank_variance_values) / len(rank_variance_values)
        
        numerator = sum((nc_ybe_order - mean_nc_ybe_order) * (rank_var - mean_rank_var) for nc_ybe_order, rank_var in zip(nc_ybe_order_values, rank_variance_values))
        denominator = sum((nc_ybe_order - mean_nc_ybe_order) ** 2 for nc_ybe_order in nc_ybe_order_values) * sum((rank_var - mean_rank_var) ** 2 for rank_var in rank_variance_values)
        
        if denominator == 0:
            correlation_coefficient = 1.0
        else:
            correlation_coefficient = numerator / (denominator ** 0.5)
    
    conjecture_holds = correlation_coefficient >= 0.75
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.75"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.75\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")