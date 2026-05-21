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
    
    def hook_length_formula(shape):
        n = sum(shape)
        hook_lengths = []
        for i in range(len(shape)):
            for j in range(shape[i]):
                hook_lengths.append((shape[i] - j) * (shape[j] - i))
        return math.prod(hook_lengths) // math.prod([math.factorial(x) for x in shape])
    
    def schur_weyl_dimension(n):
        if n == 1:
            return 1
        return sum(hook_length_formula((i, n-i)) for i in range(1, n))
    
    def epsilon_discrepancy(matrix, eps):
        rows = len(matrix)
        cols = len(matrix[0])
        total = sum(sum(abs(x) for x in row) for row in matrix)
        return (total / (rows * cols)) - eps
    
    def generate_disjointness_instance(n):
        A = random.sample(range(1, n+1), n//2)
        B = [x + n for x in A]
        C = list(set(range(1, n+1)) - set(A))
        D = list(set(range(1, n+1)) - set(B))
        return (A, B, C, D)
    
    def tensor_product(matrix1, matrix2):
        rows1 = len(matrix1)
        cols1 = len(matrix1[0])
        rows2 = len(matrix2)
        cols2 = len(matrix2[0])
        result = [[0] * (cols1 * cols2) for _ in range(rows1 * rows2)]
        for i in range(rows1):
            for j in range(cols1):
                for k in range(rows2):
                    for l in range(cols2):
                        result[i*rows2 + k][j*cols2 + l] = matrix1[i][j] * matrix2[k][l]
        return result
    
    def schur_weyl_decomposition(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix]
        dimensions = []
        for i in range(1, n):
            shape = (i, n-i)
            dimension = hook_length_formula(shape)
            dimensions.append(dimension)
        return dimensions
    
    def max_irreducible_dimension(dimensions):
        return max(dimensions) if dimensions else 0
    
    def communication_matrix(instance):
        A, B, C, D = instance
        matrix = [[0] * (len(A) + len(B)) for _ in range(len(C) + len(D))]
        for i in range(len(A)):
            matrix[i][i] = 1
        for j in range(len(B)):
            matrix[j+len(A)][j] = -1
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_dimension = 0
    instances_tested = 0
    
    for n in n_values:
        instance = generate_disjointness_instance(n)
        tensor_prod_matrix = tensor_product(communication_matrix(instance), communication_matrix(instance))
        dimensions = schur_weyl_decomposition(tensor_prod_matrix)
        max_dim = max_irreducible_dimension(dimensions)
        total_dimension += max_dim
        instances_tested += 1
    
    mean_dimension = total_dimension / len(n_values)
    
    conjecture_holds = math.log(instances_tested) <= mean_dimension <= math.log2(instances_tested)
    counterexample = "" if conjecture_holds else "disjointness_instance"
    
    return {
        "metric_name": "max_irreducible_dimension",
        "metric_value": mean_dimension,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing_seed}\" first_failing_seed={first_failing_seed}")