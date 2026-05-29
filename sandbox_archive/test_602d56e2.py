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
    
    def circuit_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] != (i & (i - 1) == 0):  # Check if i is a power of two
                count += 1
        return count
    
    def coxeter_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(2**n):
            for j in range(i, 2**n):
                if f[i] != f[j]:
                    matrix[i % n][j % n] += 1
                    matrix[j % n][i % n] += 1
        return matrix
    
    def min_order(matrix):
        n = len(matrix)
        for k in range(1, n + 1):
            found = True
            for i in range(n):
                if matrix[i][i] != k:
                    found = False
                    break
            if found:
                return k
        return n
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def is_upper_triangular(matrix):
        n = len(matrix)
        for i in range(1, n):
            for j in range(i):
                if matrix[i][j] != 0:
                    return False
        return True
    
    def order_of_matrix(matrix):
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        result = [matrix]
        for k in range(1, n + 1):
            product = [[sum(matrix[i][j] * matrix[j][k] for j in range(n)) for k in range(n)] for i in range(n)]
            if product == identity:
                return k
            result.append(product)
        return n
    
    def tropicalize(f):
        n = int(math.log2(len(f)))
        matrix = coxeter_matrix(f)
        gaussian_elimination(matrix)
        order = order_of_matrix(matrix)
        return order
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        phi_f = tropicalize(f)
        cc_f = circuit_complexity(f)
        results.append((phi_f, cc_f))
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    phi_values = [phi for phi, _ in results]
    cc_values = [cc for _, cc in results]
    correlation = sum((phi - sum(phi_values) / len(phi_values)) * (cc - sum(cc_values) / len(cc_values)) for phi, cc in results) / (len(results) * sum((phi - sum(phi_values) / len(phi_values))**2 for phi in phi_values))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")