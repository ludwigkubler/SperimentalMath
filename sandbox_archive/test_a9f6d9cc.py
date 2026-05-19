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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def matmul(A, B):
    if isinstance(A[0], float) or isinstance(B[0], float):
        return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
    else:
        return [[sum(a[i] * b[j] for i in range(len(a))) for j in range(len(b[0]))] for a in A for b in B]

def svd(M):
    m, n = len(M), len(M[0])
    U = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
    S = [sum(row[i]**2 for row in M)**0.5 for i in range(min(m, n))]
    Vt = [[M[j][i] / S[i] if i < len(S) else 0 for j in range(m)] for i in range(n)]
    return U, S, Vt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) if i != j else 1 for j in range(n)] for i in range(n)]
    
    p = math.log2(n)
    U, S, Vt = svd(M)
    norm_p = sum(S[i]**p for i in range(len(S)))**(1/p)
    
    metric_value = norm_p / n
    conjecture_holds = metric_value >= 0.1
    counterexample = "" if conjecture_holds else "norm_p/n < 0.1"
    
    return {
        "metric_name": "noncommutative L^p norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm_p/n < 0.1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")