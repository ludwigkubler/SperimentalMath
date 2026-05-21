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
                M[i][j] = 1
                M[j][i] = 1
        return M
    
    def fft_2d(M):
        n = len(M)
        if n <= 1:
            return M
        
        even_M = [fft_2d([row[::2] for row in col]) for col in zip(*M)]
        odd_M = [fft_2d([row[1::2] for row in col]) for col in zip(*M)]
        
        T = [[0] * (n // 2) for _ in range(n)]
        for k in range(n // 2):
            angle = -2 * math.pi * k / n
            c = math.cos(angle)
            s = math.sin(angle)
            for j in range(n // 2):
                T[k][j] = (even_M[k][j] + odd_M[k][j] * (c + 1j * s)) / math.sqrt(2)
        
        M_even = [row[:n // 2] for row in T]
        M_odd = [row[n // 2:] for row in T]
        return [[M_even[i][j] + M_odd[i][j] for j in range(n)] for i in range(n)]
    
    def l2_norm(M):
        n = len(M)
        sum_sq = 0
        for i in range(n):
            for j in range(n):
                sum_sq += abs(M[i][j]) ** 2
        return math.sqrt(sum_sq)
    
    n = 40
    M = generate_disjointness_matrix(n)
    F = fft_2d(M)
    norm = l2_norm(F)
    
    return {
        "metric_name": "Fourier Norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": norm >= n,
        "counterexample": "" if norm >= n else f"Norm {norm} < {n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    std_norm = math.sqrt(sum((r["metric_value"] - mean_norm) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Norm < n\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")