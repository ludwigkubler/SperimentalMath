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
    
    def generate_matrix(n: int, field_size: int):
        return [[random.randint(0, field_size - 1) for _ in range(n)] for _ in range(n)]
    
    def tensor_product(A, B):
        n = len(A)
        np_A_tensor_B = [[[A[i][k] * B[j][l] for l in range(n)] for k in range(n)] for j in range(n)]
        return np_A_tensor_B
    
    def rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        augmented_matrix = [row + matrix[i] for i, row in enumerate(matrix)]
        rank = 0
        for i in range(min(m, n)):
            if augmented_matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                    for k in range(n):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
                rank += 1
            else:
                found_pivot = False
                for j in range(i + 1, m):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
        return rank
    
    def read_twice_bp_width(matrix):
        n = len(matrix)
        width = 1
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    width += 1
        return width
    
    field_size = 5
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    A = generate_matrix(n, field_size)
    B = generate_matrix(n, field_size)
    
    np_A_tensor_B = tensor_product(A, B)
    rank_np_A_tensor_B = rank(np_A_tensor_B)
    width_bp = read_twice_bp_width(np_A_tensor_B)
    
    return {
        "metric_name": "np(A ⊗ B) - BP_ReadTwice(W(G))",
        "metric_value": rank_np_A_tensor_B - width_bp,
        "instances_tested": 1,
        "conjecture_holds": True if rank_np_A_tensor_B <= width_bp + math.log(n, 2) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) > 10)
        print(f"RESULT: FALSIFIED counterexample='metric_difference_too_large' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")