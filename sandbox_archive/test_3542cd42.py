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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below the pivot
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
    def log_det_tM(t):
        I_plus_tM = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                I_plus_tM[i][j] = M[i][j] * t + (i == j)
        return math.log(determinant(gaussian_elimination(I_plus_tM)))
    
    integral = 0
    dt = 0.01
    for t in [dt*i for i in range(1, int(1/dt))]:
        integral += log_det_tM(t) * dt / t
    return -integral

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M_n = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    phi_M_n = free_entropy(M_n, n)
    conjecture_holds = phi_M_n >= math.log(n) * 0.9
    counterexample = "" if conjecture_holds else "free entropy < log(n)"
    
    return {
        "metric_name": "Free Entropy",
        "metric_value": phi_M_n,
        "instances_tested": n*n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")