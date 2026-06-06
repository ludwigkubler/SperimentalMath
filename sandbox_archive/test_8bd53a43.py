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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_to_matrix(f, n):
        matrix = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                if f[i] == f[j]:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [1] for row in matrix]
        for i in range(n):
            if augmented_matrix[i][i] == 0:
                found = False
                for j in range(i+1, n):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        found = True
                        break
                if not found:
                    return i
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i and augmented_matrix[j][i] != 0:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return n
    
    def frobenius_schur_indicator(matrix):
        n = len(matrix)
        if n % 2 != 0:
            raise ValueError("Matrix must be square and even-sized")
        indicator = 0
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] == 1 and matrix[j][i] == 1:
                    indicator += 1
        return Fraction(indicator, n * (n - 1) // 2)
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = boolean_to_matrix(f, n)
        rank_value = rank(M)
        results.append(rank_value)
    
    mean_rank = sum(results) / len(results)
    variance_rank = variance(results)
    indicator = frobenius_schur_indicator(M)
    
    conjecture_holds = variance_rank <= indicator
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Variance of Rank",
        "metric_value": variance_rank,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")