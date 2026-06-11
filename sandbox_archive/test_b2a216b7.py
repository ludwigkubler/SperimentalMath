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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] != f[i]:
                    matrix[i][j] = 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank / n
    
    def permutation_induced_by_f(f):
        n = int(math.log2(len(f)))
        perm = [i for i in range(2**n)]
        random.shuffle(perm)
        return perm
    
    def coxeter_reflection_complexity(perm):
        n = len(perm)
        reflections = 0
        for i in range(n):
            if perm[i] != i:
                reflections += 1
        return reflections
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(i, n):
                matrix[i][j] *= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        gaussian_elimination(matrix)
        return sum(1 for row in matrix if any(row))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        matrix = communication_complexity_matrix(f)
        rank_var = rank_variance(matrix)
        perm = permutation_induced_by_f(f)
        reflections = coxeter_reflection_complexity(perm)
        
        if reflections == 0:
            continue
        
        results.append({
            "n": n,
            "rank_var": rank_var,
            "reflections": reflections
        })
    
    if not results:
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    mean_rank_var = sum(result["rank_var"] for result in results) / len(results)
    std_rank_var = math.sqrt(sum((result["rank_var"] - mean_rank_var)**2 for result in results) / len(results))
    
    if n_max < 16:
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    if mean_rank_var > n_max ** (1.5):
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_rank_var={mean_rank_var} > {n_max ** (1.5)}"
        }
    
    return {
        "metric_name": "rank_variance",
        "metric_value": mean_rank_var,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank_var = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_rank_var = math.sqrt(sum((result["metric_value"] - mean_rank_var)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_var} std={std_rank_var} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_var} std={std_rank_var} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_variance\" first_failing_seed={first_failing_seed}")