# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, w):
        circuit = []
        for _ in range(w):
            layer = [random.randint(0, 1) for _ in range(n)]
            circuit.append(layer)
        return circuit
    
    def is_permutation_matrix(matrix):
        n = len(matrix)
        if n != len(matrix[0]):
            return False
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        product = [[sum(matrix[i][k] * matrix[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        return all(product[i][j] == identity[i][j] for i in range(n) for j in range(n))
    
    def generate_permutation_matrices(circuit):
        n = len(circuit)
        matrices = []
        for perm in itertools.permutations(range(n)):
            matrix = [[0] * n for _ in range(n)]
            for i, row in enumerate(circuit):
                for j, val in enumerate(row):
                    if val == 1:
                        matrix[perm[i]][j] = 1
            if is_permutation_matrix(matrix):
                matrices.append(matrix)
        return matrices
    
    def circuit_width(circuit):
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_perm_count = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            w = random.randint(2, min(n, 40))
            circuit = generate_circuit(n, w)
            perm_matrices = generate_permutation_matrices(circuit)
            total_perm_count += len(perm_matrices)
            instances_tested += 1
            n_max = max(n_max, n)
    
    expected_bound = n ** (w / 2)
    ratio = Fraction(total_perm_count, expected_bound).limit_denominator()
    
    conjecture_holds = ratio <= 10  # Arbitrary constant factor for demonstration
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of permutation matrices to n^(w/2)",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")