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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def spectral_norm(M):
    n = len(M)
    v = [random.random() for _ in range(n)]
    v /= math.sqrt(sum(x**2 for x in v))
    for _ in range(100):  # Power iteration
        v = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
    return max(abs(v))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 40) // 8
    size_P = 2 ** n
    
    # Construct transition matrix M_P for a read-twice BP
    M_P = [[0] * size_P for _ in range(size_P)]
    for i in range(n):
        for j in range(1 << i):
            for k in range(1 << (n - i)):
                M_P[j][j ^ k] += 1
                M_P[j ^ k][j] += 1
    M_P = gaussian_elimination(M_P)
    
    norm_M_P = spectral_norm(M_P)
    
    # Construct transition matrix for IP_2 function
    M_IP2 = [[0] * (1 << n) for _ in range(1 << n)]
    for i in range(1 << n):
        for j in range(1 << n):
            if bin(i ^ j).count('1') % 2 == 0:
                M_IP2[i][j] = 1
    M_IP2 = gaussian_elimination(M_IP2)
    
    norm_M_IP2 = spectral_norm(M_IP2)
    
    return {
        "metric_name": "spectral_norm",
        "metric_value": norm_M_IP2 / math.log(size_P),
        "instances_tested": n,
        "conjecture_holds": norm_M_IP2 > 10 * math.log(size_P),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"norm_M_IP2 <= 10 * log(size_P)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")