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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def truth_table_to_matrix(f, n):
    matrix = []
    for i in range(2**n):
        input_bits = [(i >> j) & 1 for j in range(n)]
        output_bit = f[i]
        matrix.append(input_bits + [output_bit])
    return matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        if i < n:
            pivot_row = i
            while pivot_row < m and matrix[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        for j in range(m):
            if i != j and matrix[j][i] != 0:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] += factor * matrix[i][k]
    return sum(1 for row in matrix if any(row))

def local_index(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = gaussian_elimination(matrix)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        matrix = truth_table_to_matrix(f, n)
        rank = gaussian_elimination(matrix)
        local_idx = local_index(matrix)
        results.append({
            "n": n,
            "rank": rank,
            "local_index": local_idx
        })
    min_local_idx = min(result["local_index"] for result in results)
    max_rank = max(result["rank"] for result in results)
    conjecture_holds = all(0.5 * rank <= idx <= 2 * rank for result in results for rank, idx in zip([result["rank"]] * len(results), [result["local_index"]] * len(results)))
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, rank={results[0]['rank']}, local_idx={results[0]['local_index']}"
    return {
        "metric_name": "Minimal Local Index",
        "metric_value": min_local_idx,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")