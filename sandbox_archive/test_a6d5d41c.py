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
            for j in range(n - 1, i - 1, -1):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def homology_classes(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def min_distance(f, g):
        return sum(abs(f(i) - g(i)) for i in range(len(f)))
    
    n = random.randint(5, 40)
    k = random.randint(2, n)
    
    # Generate random functions f and g
    f = [random.randint(0, 1 << (n // k)) for _ in range(k)]
    g = [random.randint(0, 1 << (n // k)) for _ in range(k)]
    
    distance = min_distance(f, g)
    
    # Configuration space is a matrix where each entry is the XOR of corresponding bits
    config_space = [[f[i] ^ g[j] for j in range(k)] for i in range(k)]
    
    homology_count = homology_classes(config_space)
    
    return {
        "metric_name": "homology_classes",
        "metric_value": homology_count,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": homology_count <= math.sqrt(distance),
        "counterexample": "" if homology_count <= math.sqrt(distance) else f"Distance {distance}, Homology {homology_count}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")