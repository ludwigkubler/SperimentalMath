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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = None
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is None:
            continue
        
        # Swap the current row with the pivot row
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        
        # Eliminate non-zero entries below the pivot
        for j in range(rank + 1, rows):
            factor = -matrix[j][i] / matrix[rank][i]
            for k in range(cols):
                if matrix[rank][k] == 0:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] += factor * matrix[rank][k]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quantum_representation(f):
        n = int(math.log2(len(f)))
        Q_f = [[0] * (2**n) for _ in range(2**n)]
        for x in range(2**n):
            for y in range(2**n):
                if f[x] == f[y]:
                    Q_f[x][y] = 1
        return Q_f
    
    def entanglement_matrix(Q_f):
        n = int(math.log2(len(Q_f)))
        M_f = [[0] * (2**n) for _ in range(2**n)]
        for x in range(2**n):
            for y in range(2**n):
                if Q_f[x][y] == 1:
                    M_f[x][y] = 1
        return M_f
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = None
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            
            # Swap the current row with the pivot row
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            
            # Eliminate non-zero entries below the pivot
            for j in range(rank + 1, rows):
                factor = -matrix[j][i] / matrix[rank][i]
                for k in range(cols):
                    if matrix[rank][k] == 0:
                        matrix[j][k] = 0
                    else:
                        matrix[j][k] += factor * matrix[rank][k]
        
        rank += 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    Q_f = quantum_representation(f)
    M_f = entanglement_matrix(Q_f)
    
    rank_M_f = gaussian_elimination(M_f)
    size_Q_f = len(Q_f)
    
    return {
        "metric_name": "Rank of Entanglement Matrix",
        "metric_value": rank_M_f,
        "instances_tested": 1,
        "conjecture_holds": rank_M_f <= math.log2(size_Q_f),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(arg) for arg in sys.argv[1:]]
    else:
        # Generate a list of 30 prime numbers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")