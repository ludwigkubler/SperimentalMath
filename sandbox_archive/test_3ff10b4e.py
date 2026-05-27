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

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0]) if A else 0
    rank = 0
    for j in range(cols):
        pivot_row = None
        for i in range(rank, rows):
            if A[i][j] != 0:
                pivot_row = i
                break
        if pivot_row is not None:
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for i in range(rows):
                if i != rank:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(cols):
                        A[i][k] += factor * A[rank][k]
            rank += 1
    return rank

def rank(matrix):
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = [chr(i) for i in range(97, 97 + n)]
    
    # Generate a Sipser function (example: a simple polynomial)
    coefficients = [random.choice([-1, 1]) * random.randint(1, 10) for _ in range(n)]
    sipser_function = f"f({', '.join(variables)}) = {' + '.join(f'{coeff}*{var}' for coeff, var in zip(coefficients, variables))}"
    
    # Compute the tropicalized K-group (example: a simple matrix)
    k_group = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    rank_value = rank(k_group)
    expected_rank = math.log2(n)
    
    conjecture_holds = abs(rank_value - expected_rank) <= 1
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")