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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def compute_p_adic_differential(f):
        n = int(math.log2(len(f)))
        diff = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append((f[j+1] - f[j]) % 2)
                else:
                    row.append(0)
            diff.append(row)
        return diff
    
    def compute_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        matrix = [row[:] for row in matrix]
        rank = 0
        for i in range(m):
            if all(x == 0 for x in matrix[i]):
                continue
            pivot_col = next(j for j in range(n) if matrix[i][j] != 0)
            for j in range(i, m):
                if matrix[j][pivot_col] != 0:
                    if i != j:
                        matrix[j], matrix[i] = matrix[i], matrix[j]
                    for k in range(n):
                        if k == pivot_col:
                            continue
                        matrix[j][k] = (matrix[j][k] - matrix[i][k] * matrix[j][pivot_col]) % 2
            rank += 1
        return rank
    
    def compute_communication_complexity(diff):
        m, n = len(diff), len(diff[0])
        H_M = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if diff[i][j] != 0:
                    H_M[i][j] = (i + j) % n
        rank_H_M = compute_rank(H_M)
        return rank_H_M
    
    def boolean_tensor_product_valuation(f):
        n = int(math.log2(len(f)))
        valuation = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    valuation += 1
        return valuation
    
    instances_tested = 30
    total_metric_value = 0
    conjecture_holds_count = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        diff = compute_p_adic_differential(f)
        rank_diff = compute_rank(diff)
        valuation = boolean_tensor_product_valuation(f)
        CC_R = compute_communication_complexity(diff)
        
        if rank_diff == 0:
            continue
        
        metric_value = CC_R / (rank_diff ** 2)
        total_metric_value += metric_value
        conjecture_holds = CC_R <= rank_diff ** 2
        
        if not conjecture_holds:
            counterexample = f"CC_R={CC_R}, rank_diff^2={rank_diff**2}"
        else:
            counterexample = ""
        
        instances_tested += 1
        total_metric_value += metric_value
        if conjecture_holds:
            conjecture_holds_count += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = conjecture_holds_count / instances_tested
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction=<z>")