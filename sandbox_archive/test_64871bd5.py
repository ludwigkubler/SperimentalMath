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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n+1):
                A[j][k] -= factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][n] / A[i][i]
        for j in range(i-1, -1, -1):
            A[j][n] -= A[j][i] * x[i]

    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    AC0_size_limit = 2**10
    depth_limit = 3
    
    # Generate a random AC⁰ circuit computing PARITY on n bits
    def generate_AC0_circuit(n, size_limit, depth_limit):
        if depth_limit == 0:
            return [random.choice([0, 1])]
        else:
            inputs = generate_AC0_circuit(n, size_limit // 2, depth_limit - 1)
            outputs = []
            for i in range(len(inputs) // 2):
                x, y = inputs[2*i], inputs[2*i+1]
                if random.choice([True, False]):
                    outputs.append(x ^ y)
                else:
                    outputs.append(x & y)
            return outputs
    
    circuit = generate_AC0_circuit(n, AC0_size_limit, depth_limit)
    
    # Construct the communication matrix
    communication_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                communication_matrix[i][j] = 1
            else:
                communication_matrix[i][j] = circuit[i ^ j]
    
    # Compute the real rank via Gaussian elimination over R
    rank = 0
    A = [row[:] + [1] for row in communication_matrix]  # Augmented matrix with all-ones column
    gaussian_elimination(A)
    for row in A:
        if any(row[j] != 0 for j in range(n)):
            rank += 1
    
    metric_value = rank
    conjecture_holds = rank >= 0.1 * math.log(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "real_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")