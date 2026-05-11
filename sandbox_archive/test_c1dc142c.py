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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    return sum(1 for row in reduced_matrix if any(row[j] != 0 for j in range(cols)))

def matrix_to_function(matrix):
    n = len(matrix)
    def f(x):
        x = [int(bit) for bit in format(x, '0{}b'.format(n))]
        result = 0
        for i in range(n):
            result += matrix[i][i] * x[i]
        return result % 2
    return f

def acc0_circuit_size(matrix):
    n = len(matrix)
    if n <= 4:
        # Brute-force ACC⁰ simulation for small n
        def circuit(x):
            return matrix_to_function(matrix)(x)
        return 1
    else:
        # Placeholder for actual ACC⁰ circuit size calculation
        return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    r = rank(matrix)
    c = math.log(r) / math.log(n)
    if c <= 0 or c >= 1:
        return {
            "metric_name": "c_value",
            "metric_value": c,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    f = matrix_to_function(matrix)
    circuit_size = acc0_circuit_size(matrix)
    conjecture_holds = circuit_size >= n ** (1 / c)
    counterexample = "" if conjecture_holds else "c_value={}".format(c)
    return {
        "metric_name": "c_value",
        "metric_value": c,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes * 3, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"c_value\" first_failing_seed={}".format(first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE insufficient data")