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
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements
        pivot = A[i][i]
        for j in range(n):
            if j != i:
                factor = -A[j][i] / pivot
                for k in range(n):
                    A[j][k] += factor * A[i][k]
    return sum(1 for row in A if any(row[j] != 0 for j in range(n)) and all(row[j] == 0 for j in range(i)))

def lattice_width(A, B):
    n = len(A)
    rank = gaussian_elimination(A)
    width = max(rank, n - rank)
    return width

def construct_lattice(G):
    n = len(G)
    A = [[0] * (n + 1) for _ in range(n)]
    B = [0] * (n + 1)
    
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                A[i][j] = 1
                A[j][i] = 1
                B[i] += 1
                B[j] += 1
    
    return A, B

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = 0
        
        A, B = construct_lattice(G)
        
        width = lattice_width(A, B)
        expected_width = n ** (3/4) * math.log2(n + 1) ** 2
        if width > expected_width:
            return {
                "metric_name": "Lattice Width",
                "metric_value": width,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, lattice_width={width} > {expected_width}"
            }
    
    mean_width = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_width) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for result in results if result <= expected_width) / len(results)
    
    return {
        "metric_name": "Lattice Width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "conjecture_holds" in result and not result["conjecture_holds"]:
            break
        
        results.append(result["metric_value"])
    
    mean_width = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_width) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for result in results if result <= expected_width) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[0]}, lattice_width={results[0]} > {expected_width}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")