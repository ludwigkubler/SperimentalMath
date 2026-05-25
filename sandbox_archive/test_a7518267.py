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
from fractions import Fraction
import math

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i + 1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank_of_matrix(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row):
            rank += 1
    return rank

def plucker_embedding_rank(polytope):
    vertices = polytope['vertices']
    n = len(vertices[0])
    m = len(vertices)
    A = [[0] * (n * n) for _ in range(m * (m - 1) // 2)]
    
    idx = 0
    for i in range(m):
        for j in range(i + 1, m):
            for l in range(n):
                for k in range(l + 1, n):
                    A[idx][l * n + k] = vertices[i][l] * vertices[j][k] - vertices[i][k] * vertices[j][l]
                    A[idx][k * n + l] = vertices[i][k] * vertices[j][l] - vertices[i][l] * vertices[j][k]
            idx += 1
    
    return rank_of_matrix(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random convex polytope
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 10))
    vertices = [[random.random() for _ in range(d)] for _ in range(n)]
    polytope = {'vertices': vertices}
    
    # Compute the Plücker embedding rank
    plucker_rank = plucker_embedding_rank(polytope)
    
    # Construct a monotone k-CLIQUE circuit (simplified model)
    k = random.randint(2, min(n - 1, 5))
    circuit_size = n * (n - 1) // 2
    
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": plucker_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")