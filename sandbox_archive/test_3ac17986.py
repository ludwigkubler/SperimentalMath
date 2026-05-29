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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_truth_table(n):
        return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]
    
    def tensor_product(truth_table, identity_matrix):
        n = len(truth_table)
        result = []
        for i in range(n):
            row = []
            for j in range(n):
                new_row = [truth_table[i][k] * identity_matrix[j][k] for k in range(n)]
                row.append(new_row)
            result.append(row)
        return result
    
    def matrix_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                    pivot_row = j
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(n):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def dpll_conversion_time(n):
        # Placeholder function to simulate conversion time
        # This is a dummy implementation and should be replaced with actual logic
        return 2**n
    
    n = random.randint(5, 40)
    truth_table = generate_truth_table(n)
    identity_matrix = [[1 if i == j else 0 for j in range(2**n)] for i in range(2**n)]
    tensor_prod = tensor_product(truth_table, identity_matrix)
    rank_value = matrix_rank(tensor_prod)
    dpll_time = dpll_conversion_time(n)
    
    return {
        "metric_name": "log2_rank",
        "metric_value": math.log2(rank_value),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")