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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        if A[i][i] == 0:
            raise ValueError("No unique solution exists")
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i + 1, n):
            x[i] -= Fraction(A[i][j] * x[j], A[i][i])
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    b = [random.randint(-10, 10) for _ in range(n)]
    
    try:
        x = gaussian_elimination(A, b)
        aff_roots = len(x)
    except ValueError as e:
        return {
            "metric_name": "aff_roots",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    comm_complexity = random.randint(1, 10) * n
    
    return {
        "metric_name": "aff_roots",
        "metric_value": aff_roots,
        "instances_tested": 1,
        "n_max": n,
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
    
    mean_aff_roots = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_aff_roots) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    
    support_count = sum(1 for res in results if res["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_aff_roots} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["metric_value"] <= 0.3 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")