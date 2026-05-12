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
    
    def R_transform_inv(a):
        n = len(a)
        if n == 1:
            return a[0]
        b = [a[i] - sum(a[j] * b[j - i - 1] for j in range(i)) / (i + 1) for i in range(n)]
        c = [b[i] / (i + 1) for i in range(n)]
        return c
    
    def free_cumulants(M):
        n, m = len(M), len(M[0])
        R = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                R[i][j] = M[i][j]
        for k in range(1, n + m - 1):
            for i in range(k + 1):
                j = k - i
                if i < n and j < m:
                    R[i][j] -= sum(R[x][y] * R[i - x][j - y] for x in range(i) for y in range(j)) / (i * j)
        return [R_transform_inv(row) for row in R]
    
    def communication_complexity(n):
        # Simplified model of communication complexity for DISJ_n
        return n
    
    def generate_DISJ_n(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    n = random.randint(5, 40)
    M = generate_DISJ_n(n)
    cumulants = free_cumulants(M)
    mu_M = sum(abs(c) for c in cumulants)
    R_f = communication_complexity(n)
    
    conjecture_holds = mu_M >= 0.9 * n
    counterexample = "" if conjecture_holds else f"mu_M={mu_M} < 0.9n"
    
    return {
        "metric_name": "μ(M)",
        "metric_value": mu_M,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu_M = sum(res["metric_value"] for res in results) / len(results)
    std_mu_M = math.sqrt(sum((res["metric_value"] - mean_mu_M)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu_M} std={std_mu_M} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mu_M < 0.9n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")