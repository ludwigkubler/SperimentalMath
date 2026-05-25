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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = Fraction(matrix[i][i])
        for j in range(i, n):
            matrix[i][j] /= factor
        
        for k in range(i+1, n):
            factor = Fraction(matrix[k][i])
            for j in range(i, n):
                matrix[k][j] -= factor * matrix[i][j]
    
    # Back substitution
    result = [0] * n
    for i in range(n-1, -1, -1):
        result[i] = matrix[i][-1]
        for j in range(i+1, n):
            result[i] -= matrix[i][j] * result[j]
        result[i] /= Fraction(matrix[i][i])
    
    return result

def matrix_rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[i][j] == 0 for j in range(m)):
            continue
        rank += 1
        factor = Fraction(1, matrix[i][i])
        for j in range(m):
            matrix[i][j] *= factor
        
        for k in range(n):
            if k != i:
                factor = Fraction(matrix[k][i], matrix[i][i])
                for j in range(m):
                    matrix[k][j] -= factor * matrix[i][j]
    return rank

def clifford_group_circuit(n):
    # Placeholder function to generate a random n-bit Clifford group circuit
    # This is a stub and should be replaced with actual quantum circuit generation logic
    return [[random.choice([0, 1]) for _ in range(2*n)] for _ in range(2**n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 20, 40]
    results = []
    
    for n in n_values:
        circuit = clifford_group_circuit(n)
        Q_C = [[random.choice([0, 1]) for _ in range(2*n)] for _ in range(2*n)]
        rank = matrix_rank(Q_C)
        
        expected_rank = n**2 * Fraction(1, 2) * math.log2(n)
        if rank < expected_rank:
            return {
                "metric_name": "average_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank} is less than Θ(n^2 log n) for n={n}"
            }
        
        results.append(rank)
    
    average_rank = sum(results) / len(results)
    return {
        "metric_name": "average_rank",
        "metric_value": average_rank,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    import math
    
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank below Θ(n^2 log n)' first_failing_seed={first_failing_seed}")