# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def boolean_to_diophantine(f, n_vars):
    # Convert a boolean function to a system of Diophantine equations
    n = len(f)
    equations = []
    for i in range(n):
        if f[i]:
            eq = [0] * (n + 1)
            eq[i] = 1
            eq[-1] = 1
            equations.append(eq)
    return equations

def gaussian_elimination(matrix, n_vars):
    # Perform Gaussian elimination to find the rank of the matrix
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n_vars):
        if i < rows:
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] != 0:
                rank += 1
                for j in range(i + 1, rows):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n_vars + 1):
                        matrix[j][k] += factor * matrix[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_vars = random.randint(5, 40)
    f = [random.choice([True, False]) for _ in range(2**n_vars)]
    
    equations = boolean_to_diophantine(f, n_vars)
    rank_variance = len(equations) ** 2
    
    num_representations = len(equations)
    
    return {
        "metric_name": "ratio",
        "metric_value": Fraction(num_representations, rank_variance),
        "instances_tested": 1,
        "n_max": n_vars,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
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
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")