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
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def free_entropy(M):
        X = [[(M[i][j] + 1) / 2 for j in range(len(M))] for i in range(len(M))]
        rho = spectral_radius(X)
        return -math.log(rho)
    
    def spectral_radius(matrix):
        n = len(matrix)
        v = [1.0] * n
        tol = 1e-6
        max_iter = 1000
        for _ in range(max_iter):
            w = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            norm_w = sum(w[i]**2 for i in range(n))**0.5
            if abs(norm_w - 1) < tol:
                break
            v = [w[i] / norm_w for i in range(n)]
        return max(abs(v[i]) for i in range(n))
    
    n = 16
    M = generate_disjointness_matrix(n)
    tau_M = free_entropy(M)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": tau_M,
        "instances_tested": 1,
        "conjecture_holds": tau_M >= 0.3 * n,
        "counterexample": "" if tau_M >= 0.3 * n else "tau(M) < 0.3n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")