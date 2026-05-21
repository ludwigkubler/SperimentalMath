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
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def rank(A):
        m, n = len(A), len(A[0])
        if m == 0 or n == 0:
            return 0
        A = [list(row) for row in A]
        pivot_col = 0
        for i in range(m):
            while pivot_col < n and A[i][pivot_col] == 0:
                pivot_col += 1
            if pivot_col == n:
                break
            for j in range(i + 1, m):
                factor = A[j][pivot_col] / A[i][pivot_col]
                for k in range(pivot_col, n):
                    A[j][k] -= factor * A[i][k]
        return sum(1 for row in A if any(row))
    
    def border_rank(A):
        m, n = len(A), len(A[0])
        rank_A = rank(A)
        if rank_A == 1:
            return 1
        B = [[A[i][j] * A[j][i] for j in range(n)] for i in range(m)]
        rank_B = rank(B)
        return max(rank_A, rank_B) + 1
    
    secant_dimension = border_rank(M)
    
    metric_name = "secant_dimension_ratio"
    metric_value = secant_dimension / n
    instances_tested = 1
    conjecture_holds = metric_value >= 1
    counterexample = "" if conjecture_holds else f"Matrix: {M}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")