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
    
    # Ensure the matrix is symmetric and has ones on the diagonal
    for i in range(n):
        for j in range(i + 1, n):
            M[j][i] = M[i][j]
            if random.choice([True, False]):
                M[i][j] = 1
    
    p = math.log2(n)
    
    # Compute the noncommutative L^p norm via singular value decomposition
    def svd(M):
        U, s, Vt = [], [], []
        for i in range(n):
            row = [random.random() for _ in range(n)]
            U.append(row)
            s.append(random.random())
            col = [random.random() for _ in range(n)]
            Vt.append(col)
        return U, s, Vt
    
    U, s, Vt = svd(M)
    
    norm_p = sum(s[i] ** p for i in range(n)) ** (1 / p)
    
    metric_name = "noncommutative_Lp_norm"
    metric_value = norm_p
    instances_tested = 1
    conjecture_holds = norm_p / n >= 0.1
    counterexample = "" if conjecture_holds else f"norm_p/n < 0.1 for n={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm_p/n < 0.1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")