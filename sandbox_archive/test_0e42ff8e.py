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

def matrix_multiplication(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    for i in range(rows):
        max_row = i
        for j in range(i+1, rows):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, cols + 1):
            augmented_matrix[i][j] /= pivot
        for j in range(rows):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, cols + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    rank = sum(1 for row in augmented_matrix if any(row))
    return rank

def generate_ac0_circuit(n):
    circuit = []
    for _ in range(n):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        circuit.append(matrix)
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_ac0_circuit(n)
            rank = gaussian_elimination(circuit)
            total_rank += rank
            instances_tested += 1
    
    mean_minimal_rank = total_rank / instances_tested
    conjecture_holds = mean_minimal_rank <= n * math.log(n, 2) * 1.5  # Using a constant c=1.5 for testing
    counterexample = "" if conjecture_holds else "circuit_with_high_rank"
    
    return {
        "metric_name": "mean_minimal_rank",
        "metric_value": mean_minimal_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_minimal_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")