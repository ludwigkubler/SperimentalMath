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
    
    def matrix_dilation(M):
        n = len(M)
        I = [[0] * n for _ in range(n)]
        for i in range(n):
            I[i][i] = 1
        D = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                D[2*i][2*j] = M[i][j]
                D[2*i+1][2*j+1] = M[i][j]
        return D
    
    def noncommutative_lp_norm(M, p):
        n = len(M)
        D = matrix_dilation(M)
        trace = 0
        for i in range(n):
            for j in range(n):
                trace += abs(D[2*i][2*j] + D[2*i+1][2*j+1]) ** p
        return (trace / n) ** (1/p)
    
    def disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][(i+1)%n] = 1
        return M
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = math.log(n)
    M = disjointness_matrix(n)
    norm = noncommutative_lp_norm(M, p)
    
    metric_name = "noncommutative_lp_norm"
    metric_value = norm
    instances_tested = 1
    conjecture_holds = norm >= 0.1 * math.sqrt(n)
    counterexample = "" if conjecture_holds else f"norm={norm} < 0.1*sqrt({n})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm < 0.1*sqrt(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")