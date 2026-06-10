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
        min_comm_cost = float('inf')
        for x in range(2**n):
            y = f[x]
            comm_cost = bin(x).count('1') + bin(y).count('1')
            if comm_cost < min_comm_cost:
                min_comm_cost = comm_cost
        return min_comm_cost
    
    def truth_table_to_matrix(truth_table):
        n = int(math.log2(len(truth_table)))
        matrix = []
        for i in range(2**n):
            row = [truth_table[i]]
            for j in range(n):
                if (i & (1 << j)) != 0:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix
    
    def rank_of_matrix(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                found = False
                for j in range(i+1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found = True
                        break
                if not found:
                    return i
            for j in range(n):
                if j != i and matrix[i][j]:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def log_expression(n, w):
        return math.log(n + math.log(w))
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_boolean_function(n)
        w = communication_complexity(f)
        matrix = truth_table_to_matrix(f)
        actual_rank = rank_of_matrix(matrix)
        expected_rank = log_expression(n, w)
        results.append({
            "n": n,
            "actual_rank": actual_rank,
            "expected_rank": expected_rank
        })
    
    mean_actual_rank = sum(result["actual_rank"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["actual_rank"] - mean_actual_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["actual_rank"] - result["expected_rank"]) <= std_deviation) / len(results)
    
    return {
        "metric_name": "Rank of Noncrossing Partition Matroid",
        "metric_value": mean_actual_rank,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"Rank difference exceeds std dev: {mean_actual_rank} vs {result['expected_rank']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank difference exceeds std dev\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")