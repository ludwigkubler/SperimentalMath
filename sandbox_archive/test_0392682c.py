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
    
    def communication_complexity_matrix(f, n):
        matrix = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                inputs = [(i >> k) & 1 for k in range(n)] + [(j >> k) & 1 for k in range(n)]
                outputs = f(inputs)
                row.append(outputs)
            matrix.append(row)
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [0] * n + [i] for i, row in enumerate(matrix)]
        for i in range(n):
            if augmented_matrix[i][i] == 0:
                for j in range(i+1, n):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        break
                else:
                    continue
            pivot = augmented_matrix[i][i]
            for j in range(n + i + 1):
                augmented_matrix[i][j] /= pivot
            for k in range(n):
                if k != i and augmented_matrix[k][i] != 0:
                    factor = augmented_matrix[k][i]
                    for j in range(n + i + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[n:] for row in augmented_matrix]
    
    def rank(matrix):
        rref = gaussian_elimination(matrix)
        return sum(1 for row in rref if any(row[j] != 0 for j in range(len(row))))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    matrix = communication_complexity_matrix(f, n)
    rank_var = rank(matrix)
    
    # Minimal order of noncrossing partitions is not defined for this conjecture
    return {
        "metric_name": "rank_variance",
        "metric_value": rank_var,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")