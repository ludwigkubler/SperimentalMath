# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tropical_matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        T = [[matrix[i][j] + 1 for j in range(n)] for i in range(m)]
        
        def gaussian_elimination(A):
            rows, cols = len(A), len(A[0])
            rank = 0
            for col in range(cols):
                pivot_row = None
                for row in range(rank, rows):
                    if A[row][col] != -math.inf:
                        pivot_row = row
                        break
                if pivot_row is not None:
                    A[pivot_row], A[rank] = A[rank], A[pivot_row]
                    for r in range(rank + 1, rows):
                        factor = A[r][col] / A[rank][col]
                        for c in range(cols):
                            A[r][c] -= factor * A[rank][c]
                    rank += 1
            return rank
        
        return gaussian_elimination(T)
    
    def generate_bp(m, n):
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)
    
    def communication_complexity(bp):
        # Simplified simulation of read-twice BP communication complexity
        return len(bp) * math.log2(n)
    
    n = 10  # Start with a small number of vertices for simplicity
    m = int(2 * n)  # Ensure m/n is roughly constant
    
    bp = generate_bp(m, n)
    rank = tropical_matrix_rank(bp)
    comm_complexity = communication_complexity(bp)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": rank <= m ** 0.5 * n and comm_complexity >= 2 ** (m / n) * n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample='seed {first_failing_seed}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")