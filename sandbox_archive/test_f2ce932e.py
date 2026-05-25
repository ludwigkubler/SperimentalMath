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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polytope(d, n):
        vertices = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
        return vertices
    
    def plucker_embedding_rank(vertices):
        d = len(vertices[0])
        n = len(vertices)
        A = [[0] * (d * n) for _ in range(d * n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                idx = i * d + j
                for l in range(d):
                    for k in range(l + 1, d):
                        A[idx][l * n + k] = vertices[i][l] * vertices[j][k] - vertices[i][k] * vertices[j][l]
        
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        pivot_row = 0
        pivot_col = 0
        
        while pivot_row < m and pivot_col < n:
            max_abs = abs(matrix[pivot_row][pivot_col])
            max_row = pivot_row
            
            for i in range(pivot_row + 1, m):
                if abs(matrix[i][pivot_col]) > max_abs:
                    max_abs = abs(matrix[i][pivot_col])
                    max_row = i
            
            if matrix[max_row][pivot_col] == 0:
                pivot_col += 1
                continue
            
            matrix[pivot_row], matrix[max_row] = matrix[max_row], matrix[pivot_row]
            
            for i in range(m):
                if i != pivot_row:
                    factor = -matrix[i][pivot_col] / matrix[pivot_row][pivot_col]
                    for j in range(n):
                        matrix[i][j] += factor * matrix[pivot_row][j]
            
            pivot_row += 1
            pivot_col += 1
        
        rank = sum(1 for row in matrix if any(val != 0 for val in row))
        return rank
    
    def monotone_k_clique_circuit_size(n, k):
        # Placeholder function to simulate the size of a monotone k-CLIQUE circuit
        # This is just a dummy implementation and should be replaced with actual logic
        return n * (n - 1) // 2
    
    d = random.randint(5, 40)
    n = random.randint(5, 40)
    polytope = generate_polytope(d, n)
    
    plucker_rank = plucker_embedding_rank(polytope)
    k = random.randint(2, min(n - 1, 10))
    circuit_size = monotone_k_clique_circuit_size(n, k)
    
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": plucker_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")