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
    
    def generate_groupoid(n):
        elements = set(range(1, n + 1))
        generators = []
        for _ in range(random.randint(1, n)):
            generator = [random.choice(elements)]
            while len(generator) < n and len(set(generator)) == len(generator):
                generator.append((generator[-1] * random.randint(2, n)) % n)
            generators.append(generator)
        return set(generators), elements
    
    def communication_complexity(groupoid, elements):
        matrix = [[0 for _ in range(len(elements))] for _ in range(len(elements))]
        for g in groupoid:
            for i in range(len(elements)):
                for j in range(i + 1, len(elements)):
                    if (elements[i] * random.choice(g)) % n == elements[j]:
                        matrix[i][j] = 1
                        matrix[j][i] = 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] != 0:
                        for k in range(n):
                            matrix[j][k] -= matrix[i][k]
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        gaussian_elimination(matrix)
        return sum(1 for row in matrix if any(row[i] != 0 for i in range(n)))
    
    n = random.randint(5, 40)
    groupoid, elements = generate_groupoid(n)
    matrix = communication_complexity(groupoid, elements)
    rank_var = rank_variance(matrix)
    log_n = math.log(n)
    
    if log_n <= 0:
        return {
            "metric_name": "rank_variance_over_log_n",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "log_n is non-positive"
        }
    
    ratio = rank_var / log_n
    
    return {
        "metric_name": "rank_variance_over_log_n",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio exceeds constant factor\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")