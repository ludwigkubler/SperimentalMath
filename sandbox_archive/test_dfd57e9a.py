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
    for i in range(rows):
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / pivot
            for k in range(cols):
                matrix[j][k] += factor * matrix[i][k]
    return matrix

def compute_boundary_matrix(rows, max_distance):
    n = len(rows)
    boundary_matrix = [[0] * (n * (n - 1) // 2) for _ in range(n)]
    edge_index = 0
    for i in range(n):
        for j in range(i + 1, n):
            distance = sum(1 for a, b in zip(rows[i], rows[j]) if a != b)
            if distance <= max_distance:
                boundary_matrix[i][edge_index] = -1
                boundary_matrix[j][edge_index] = 1
                edge_index += 1
    return boundary_matrix

def compute_persistence(boundary_matrix):
    n = len(boundary_matrix)
    matrix = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(n):
        for j in range(i, n):
            if boundary_matrix[i][j] != 0:
                matrix[i][j + 1] += boundary_matrix[i][j]
                matrix[j + 1][i] -= boundary_matrix[i][j]
    matrix = gaussian_elimination(matrix)
    birth_death_pairs = []
    for i in range(n):
        for j in range(i + 1, n + 2):
            if matrix[i][j] != 0:
                birth = None
                death = None
                for k in range(j - 1, -1, -1):
                    if matrix[k][i] == 0 and matrix[k][j] != 0:
                        birth = k
                        break
                for k in range(j + 1, n + 2):
                    if matrix[k][i] != 0 and matrix[k][j] == 0:
                        death = k
                        break
                if birth is not None and death is not None:
                    birth_death_pairs.append((birth, death))
    return sum(death - birth for birth, death in birth_death_pairs)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5, 6]
    results = []
    
    for n in n_values:
        N = 2 ** n
        k = math.ceil(math.sqrt(N))
        
        M_DISJ_n = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
        M_IP_n = [[(i & j).bit_count() % 2 for j in range(N)] for i in range(N)]
        M_EQ_n = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
        M_RAND_n = [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]
        
        for matrix in [M_DISJ_n, M_IP_n, M_EQ_n, M_RAND_n]:
            rows = random.sample(matrix, k)
            max_distance = int(0.75 * N)
            boundary_matrix = compute_boundary_matrix(rows, max_distance)
            persistence = compute_persistence(boundary_matrix)
            
            results.append({
                "matrix_type": type(matrix).__name__,
                "n": n,
                "k": k,
                "persistence": persistence
            })
    
    mean_log2 = sum(math.log2(1 + result["persistence"] * result["k"]) for result in results) / len(results)
    cc_r_disj = 0.5 * (math.log2(n_values[-1]) - math.log2(n_values[0]))
    support_fraction = sum(1 for result in results if result["matrix_type"] == "M_DISJ_n") / len(results)
    
    conjecture_holds = mean_log2 >= 0.8 * cc_r_disj and support_fraction >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_log2",
        "metric_value": mean_log2,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")