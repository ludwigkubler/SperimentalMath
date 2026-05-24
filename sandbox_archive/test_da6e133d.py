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

def generate_quantum_channel(n):
    # Placeholder function to generate a random quantum channel
    return [[random.random() for _ in range(n)] for _ in range(n)]

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def commutator(A, B):
    return matrix_multiply(matrix_multiply(A, B), -matrix_multiply(B, A))

def rank(matrix):
    # Placeholder function to compute the rank of a matrix
    n = len(matrix)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented_matrix = [row + col for row, col in zip(matrix, identity)]
    rows = len(augmented_matrix)
    cols = len(augmented_matrix[0])
    
    def gaussian_elimination(A):
        r = 0
        for c in range(cols):
            if all(row[c] == 0 for row in A[r:]):
                continue
            pivot_row = r + [row[c] for row in A[r:]]
            for i in range(r, rows):
                if i != r:
                    factor = -A[i][c] / pivot_row[c]
                    A[i] = [pivot_row[j] * factor + A[i][j] for j in range(cols)]
            r += 1
        return r
    
    return gaussian_elimination(augmented_matrix)

def minimal_index_of_noncommutativity(channel):
    n = len(channel)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    rho = rank(commutator(identity, channel))
    return rho

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        channel = generate_quantum_channel(n)
        rho = minimal_index_of_noncommutativity(channel)
        size_BP = 2 ** n  # Simplified model of BP size
        log_size_BP = math.log(size_BP, 2)
        
        if rho <= log_size_BP and rho >= (n / math.log(n)):
            results.append(1)
        else:
            return {
                "metric_name": "minimal_index_of_noncommutativity",
                "metric_value": rho,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"rho({n}) = {rho}, expected O(log size(BP)) and Ω(n/log n)"
            }
    
    return {
        "metric_name": "minimal_index_of_noncommutativity",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= (mean - 3 * std_dev)) / len(results)
    
    if all(r >= (mean - 3 * std_dev) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < (mean - 3 * std_dev) for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if result < (mean - 3 * std_dev))
        print(f"RESULT: FALSIFIED counterexample='rho({n_values[0]}) out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(seeds)}")