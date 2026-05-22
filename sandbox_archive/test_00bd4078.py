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
    
    def generate_branching_program(n):
        nodes = [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
        edges = []
        for i in range(n-1):
            edges.append((i, i+1))
        return nodes, edges
    
    def tropicalize(mat):
        n = len(mat)
        for i in range(n):
            for j in range(n):
                if mat[i][j] == 0:
                    mat[i][j] = float('-inf')
        return mat
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1] for row in matrix]
        for i in range(m):
            if augmented_matrix[i][i] == 0:
                for j in range(i+1, m):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        break
                else:
                    return float('inf')
            pivot = augmented_matrix[i][i]
            for j in range(n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(m):
                if j != i and augmented_matrix[j][i] != 0:
                    factor = augmented_matrix[j][i]
                    for k in range(n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return sum(1 for row in augmented_matrix if row[-1] != 0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        nodes, edges = generate_branching_program(n)
        size_P = len(nodes)
        tropicalized_matrix = [[nodes[i][j] ^ nodes[j][i] for j in range(size_P)] for i in range(size_P)]
        rank_value = rank(tropicalized_matrix)
        results.append({
            "n": n,
            "size_P": size_P,
            "rank_value": rank_value
        })
    
    metric_value = sum(result["rank_value"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(
        abs(math.log(result["size_P"]) - result["rank_value"]) <= 3 and result["rank_value"] >= math.ceil(result["n"] ** 0.25)
        for result in results
    )
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Geometric Quantization",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")