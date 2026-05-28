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
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        for j in range(cols):
            A[i][j] /= factor
        for j in range(rows):
            if i != j:
                factor = A[j][i]
                for k in range(cols):
                    A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def quotient_sheaf(bp):
    n = len(bp)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            A[i][j] = bp[j]
            A[j][i] = bp[j]
    return gaussian_elimination(A)

def trivial_bp(n):
    return [1 if i == 0 else 0 for i in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = [random.randint(0, 1) for _ in range(n)]
        rank = quotient_sheaf(bp)
        if rank > math.log2(2**n):
            counterexample = f"BP of size {n} with rank {rank}"
            return {
                "metric_name": "quotient_sheaf_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        results.append(rank)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = 1.0
    
    return {
        "metric_name": "quotient_sheaf_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= math.log2(2**len(seeds))) / len(results)
    
    if all(r <= math.log2(2**len(seeds)) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > math.log2(2**len(seeds)) for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"BP of size {len(seeds)} with rank {max(results)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")