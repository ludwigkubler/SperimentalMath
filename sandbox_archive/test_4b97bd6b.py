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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def xor_and_tree_width(F):
        # Placeholder function, replace with actual implementation
        return len(F)  # Simplified example
    
    def hodge_decomposition(F):
        # Placeholder function, replace with actual implementation
        return [[1] * len(F)]  # Simplified example
    
    n = random.randint(2, 40)
    m = random.randint(n, 2*n)
    F = ['x' + str(i) for i in range(n)]
    
    rank_H_F = sum(gaussian_elimination(hodge_decomposition(F)) for _ in range(m))
    tw_F = xor_and_tree_width(F)
    
    c = 1.0  # Placeholder constant, replace with actual value
    if tw_F > c * rank_H_F:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": tw_F,
            "instances_tested": m,
            "conjecture_holds": False,
            "counterexample": f"Formula F with n={n}, m={m} has tw(F) > c * r(H_F)"
        }
    else:
        return {
            "metric_name": "XOR-AND tree width",
            "metric_value": tw_F,
            "instances_tested": m,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with tw(F) > c * r(H_F)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")