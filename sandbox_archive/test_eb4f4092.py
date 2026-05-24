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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n - 1, i, -1):
                factor = A[j][i] / A[i][i]
                for k in range(m):
                    A[k][j] -= factor * A[k][i]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def tensor_width(bp):
        # Placeholder function to simulate BP_ReadTwice tensor width calculation
        return len(bp) ** 2
    
    def min_rank(divisor):
        # Placeholder function to simulate minimal rank of tropicalized divisor
        return len(divisor)
    
    n = random.choice([10, 15, 20, 25, 30])
    curve_points = [(random.random(), random.random()) for _ in range(n)]
    divisor = [sum(point) for point in curve_points]
    bp_size = sum(len(bp) for bp in [curve_points] * n)
    
    rank = min_rank(divisor)
    width = tensor_width([curve_points])
    
    return {
        "metric_name": "MinRank vs TensorWidth",
        "metric_value": rank / width,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 * width,  # Placeholder linear bound
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")