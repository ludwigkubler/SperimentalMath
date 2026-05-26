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
    
    def generate_read_twice_bp(size):
        return [random.choice([0, 1]) for _ in range(2 * size)]
    
    def frege_proof_width(formula):
        if isinstance(formula, list):
            return max(frege_proof_width(subformula) for subformula in formula)
        else:
            return 1
    
    def compute_entanglement_tensor(bp):
        n = len(bp) // 2
        tensor = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if bp[i] == bp[j]:
                    tensor[i][j] = 1
        return tensor
    
    def min_rank(tensor):
        m, n = len(tensor), len(tensor[0])
        rank = 0
        U = [row[:] for row in tensor]
        V = [row[:] for row in tensor]
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                factor = matrix[i][i]
                for j in range(cols):
                    matrix[i][j] /= factor
                for j in range(rows):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[i][k]
        
        gaussian_elimination(U)
        gaussian_elimination(V)
        
        rank_u, rank_v = 0, 0
        for row in U:
            if any(row):
                rank_u += 1
        for col in V:
            if any(col):
                rank_v += 1
        
        return min(rank_u, rank_v)
    
    size = random.randint(5, 40)
    bp = generate_read_twice_bp(size)
    entanglement_tensor = compute_entanglement_tensor(bp)
    rank = min_rank(entanglement_tensor)
    
    lower_bound = size
    upper_bound = math.log2(size) ** 2
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = lower_bound <= rank <= upper_bound
    counterexample = "" if conjecture_holds else f"rank={rank}, expected=[{lower_bound}, {upper_bound}]"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank below bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")