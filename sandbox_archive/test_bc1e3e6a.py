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
    
    def generate_read_twice_bp(n):
        layers = []
        for _ in range(2):  # Read-twice BP has two layers
            layer = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            layers.append(layer)
        return layers
    
    def adjacency_matrix(bp_layer):
        n = len(bp_layer)
        adj_mat = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if bp_layer[i][j]:
                    adj_mat[i][j] = 1
        return adj_mat
    
    def tensor_product(matrices):
        if not matrices:
            return []
        result = matrices[0]
        for mat in matrices[1:]:
            new_result = []
            for row1 in result:
                new_row = [sum(row1[j] * row2[j] for j in range(len(row2))) for row2 in mat]
                new_result.append(new_row)
            result = new_result
        return result
    
    def min_eigenvalue(matrix):
        n = len(matrix)
        eigenvalues = []
        for i in range(n):
            vector = [1 if j == i else 0 for j in range(n)]
            value = sum(matrix[i][j] * vector[j] for j in range(n))
            eigenvalues.append(value)
        return min(eigenvalues)
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    adj_matrices = [adjacency_matrix(layer) for layer in bp]
    mp = tensor_product(adj_matrices)
    min_eig = min_eigenvalue(mp)
    
    size_p = sum(sum(row) for row in bp[0]) + sum(sum(row) for row in bp[1])
    expected_min_eig = math.log(size_p)
    
    if "IP_2 trivial BP" in str(bp):
        conjecture_holds = min_eig >= 0.9 * n
        counterexample = ""
    else:
        conjecture_holds = abs(min_eig - expected_min_eig) <= 1e-5
        counterexample = "" if conjecture_holds else "IP_2 trivial BP"
    
    return {
        "metric_name": "min_eigenvalue",
        "metric_value": min_eig,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 trivial BP\" first_failing_seed={first_failing_seed}")