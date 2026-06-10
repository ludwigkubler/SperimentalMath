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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_comm_cost = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    comm_cost = bin(i ^ j).count('1')
                    max_comm_cost = max(max_comm_cost, comm_cost)
        return max_comm_cost
    
    def truth_table_to_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[0]*n for _ in range(n)]
        for i in range(2**n):
            binary_rep = f'{i:0{n}b}'
            for j in range(n):
                if binary_rep[j] == '1':
                    matrix[j][j] += 1
        return matrix
    
    def rank_of_matrix(matrix):
        n = len(matrix)
        augmented_matrix = [row + [1] for row in matrix]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            if augmented_matrix[i][i] == 0:
                return float('inf')
            for j in range(i+1, n):
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        rank = sum(1 for row in augmented_matrix if row[-1] != 0)
        return rank
    
    def log_expression(n, w):
        return math.log(n + math.log(w))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        w = communication_complexity(f)
        matrix = truth_table_to_matrix(f)
        rank = rank_of_matrix(matrix)
        expected_rank = log_expression(n, w)
        results.append({
            "n": n,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["rank"] - result["expected_rank"]) <= 1) / len(results)
    
    conjecture_holds = support_fraction >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank of Noncrossing Partition Matroid",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")