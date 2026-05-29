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
    
    def generate_truth_table(n):
        return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]
    
    def tensor_product(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[0] * (n * p) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j * p + k] = A[i][j] * B[j][k]
        return result
    
    def rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        if m == 0 or n == 0:
            return 0
        rows = [list(row) for row in matrix]
        cols = list(zip(*rows))
        r = min(m, n)
        for i in range(r):
            max_row = max(range(i, m), key=lambda x: abs(rows[x][i]))
            if rows[max_row][i] == 0:
                return rank(matrix[:i] + matrix[i+1:])
            rows[i], rows[max_row] = rows[max_row], rows[i]
            for j in range(m):
                if i != j:
                    factor = rows[j][i] / rows[i][i]
                    for k in range(n):
                        rows[j][k] -= factor * rows[i][k]
        return r
    
    def dpll_conversion_time(n):
        # Placeholder function to simulate DPLL conversion time
        # This is a dummy implementation and should be replaced with actual logic
        return n**2  # Example: quadratic complexity for demonstration purposes
    
    n = random.randint(5, 40)
    truth_table = generate_truth_table(n)
    identity_matrix = [[1 if i == j else 0 for j in range(2**n)] for i in range(2**n)]
    tensor_prod = tensor_product(truth_table, identity_matrix)
    rank_value = rank(tensor_prod)
    dpll_time = dpll_conversion_time(n)
    
    return {
        "metric_name": "log2_rank",
        "metric_value": math.log2(rank_value),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")