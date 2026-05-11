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
    
    def generate_read_twice_bp(n):
        bp = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    bp[i][j] = 1
                else:
                    bp[i][j] = random.randint(0, 1)
                    bp[j][i] = bp[i][j]
        return bp
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
            M[i], M[max_row] = M[max_row], M[i]
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                M[j] = [M[j][k] - factor * M[i][k] for k in range(n + 1)]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (M[i][-1] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
        return x
    
    def compute_transition_matrix(bp):
        n = len(bp)
        I = [[0] * n for _ in range(n)]
        for i in range(n):
            I[i][i] = 1
        T = [I]
        for _ in range(2):
            T.append(matrix_multiply(T[-1], bp))
        return T
    
    def compute_moments(T):
        n = len(T[0])
        moments = []
        for t in T:
            moment = sum(sum(t[i][j] * t[j][i] for j in range(n)) for i in range(n))
            moments.append(moment)
        return moments
    
    def approximate_free_cumulant(moments):
        n = len(moments)
        if n == 1:
            return moments[0]
        cumulants = [moments[0]]
        for k in range(1, n):
            cumulant = (moments[k] - sum(cumulants[i] * cumulants[k-1-i] for i in range(k))) / (k + 1)
            cumulants.append(cumulant)
        return cumulants[-1]
    
    def is_ip2(bp):
        n = len(bp)
        for i in range(n):
            if bp[i][i] != 1:
                return False
            for j in range(i+1, n):
                if bp[i][j] != bp[j][i]:
                    return False
        return True
    
    def log_size(bp):
        n = len(bp)
        return math.log(n * (n + 1) // 2)
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    T = compute_transition_matrix(bp)
    moments = compute_moments(T)
    free_cumulant = approximate_free_cumulant(moments)
    
    if is_ip2(bp):
        expected = n / 2
        conjecture_holds = free_cumulant >= expected
        counterexample = "" if conjecture_holds else f"IP_2 failed with n={n}, free_cumulant={free_cumulant}"
    else:
        expected = log_size(bp) + 10
        conjecture_holds = free_cumulant <= expected
        counterexample = "" if conjecture_holds else f"General BP failed with n={n}, free_cumulant={free_cumulant}"
    
    return {
        "metric_name": "Free Cumulant",
        "metric_value": free_cumulant,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")