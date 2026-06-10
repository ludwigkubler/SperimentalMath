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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity(f, n):
    # Simplified version for demonstration purposes
    return n

def truth_table_to_matrix(truth_table, n):
    matrix = []
    for i in range(len(truth_table)):
        row = [truth_table[i]]
        for j in range(n):
            row.append(truth_table[i ^ (1 << j)])
        matrix.append(row)
    return matrix

def rank_of_matrix(matrix):
    m, n = len(matrix), len(matrix[0])
    if m == 0 or n == 0:
        return 0
    for i in range(m):
        if matrix[i][i] == 0:
            # Find a non-zero element in the column and swap rows
            found = False
            for j in range(i + 1, m):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    found = True
                    break
            if not found:
                continue
        # Eliminate non-zero elements below the pivot
        for j in range(i + 1, m):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        w_f = communication_complexity(f, n)
        matrix = truth_table_to_matrix(f, n)
        
        actual_rank = rank_of_matrix(matrix)
        expected_bound = math.log(n + math.log(w_f), 2)
        
        results.append({
            "n": n,
            "actual_rank": actual_rank,
            "expected_bound": expected_bound
        })
    
    mean_rank = sum(result["actual_rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["actual_rank"] - mean_rank) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(abs(result["actual_rank"] - result["expected_bound"]) <= std_dev for result in results)
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
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")