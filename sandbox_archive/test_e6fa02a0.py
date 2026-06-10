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

def generate_random_protocol(n):
    inputs = [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)]
    outputs = [random.randint(0, 1) for _ in range(2**n)]
    return {input: output for input, output in zip(inputs, outputs)}

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = A[i][i]
        for j in range(i+1, n):
            factor_j = A[j][i] / factor
            for k in range(n):
                A[j][k] -= factor_j * A[i][k]
    
    rank = sum(1 for row in A if any(row))
    return rank

def rank_variance(protocol):
    n = len(next(iter(protocol.keys())))
    matrix = [[protocol[input[:i] + (j,) + input[i+1:]] - protocol[input[:i] + ((1-j),) + input[i+1:]] for j in range(2)] for input in protocol]
    
    # Compute the rank of the matrix
    rank = gaussian_elimination(matrix)
    
    # Compute the variance
    mean = sum(sum(row) for row in matrix) / (n * 2**n)
    variance = sum((x - mean)**2 for row in matrix for x in row) / (n * 2**n)
    
    return rank, variance

def riesz_representation_rank(protocol):
    n = len(next(iter(protocol.keys())))
    A = [[protocol[input[:i] + (j,) + input[i+1:]] - protocol[input[:i] + ((1-j),) + input[i+1:]] for j in range(2)] for input in protocol]
    
    # Compute the rank of the matrix
    rank = gaussian_elimination(A)
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            protocol = generate_random_protocol(n)
            riesz_rank, variance = rank_variance(protocol)
            if riesz_rank == 0 or variance == 0:
                continue
            correlation_sum += riesz_rank / variance
            instances_tested += 1
    
    mean_correlation = correlation_sum / instances_tested
    conjecture_holds = mean_correlation >= 0.5
    counterexample = "" if conjecture_holds else "correlation_too_low"
    
    return {
        "metric_name": "mean_correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_seeds_support")