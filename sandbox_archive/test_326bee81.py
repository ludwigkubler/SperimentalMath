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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def free_entropy(M, n):
    t_values = [0.01 * (i + 1) for i in range(100)]
    total = 0
    for t in t_values:
        I_plus_tM = [[1 if i == j else 0 + t * M[i][j] for j in range(n)] for i in range(n)]
        det_I_plus_tM = determinant(gaussian_elimination(I_plus_tM))
        total += math.log(det_I_plus_tM) / t
    return -total

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        M_n = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        phi_M_n = free_entropy(M_n, n)
        if phi_M_n < (math.log(n) * 0.5):
            return {
                "metric_name": "free_entropy",
                "metric_value": phi_M_n,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"phi(M_{n}) = {phi_M_n} < 0.5 * log({n})"
            }
        results.append(phi_M_n)
    return {
        "metric_name": "free_entropy",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= (math.log(n_values[0]) * 0.5)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"phi(M_n) < 0.5 * log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")