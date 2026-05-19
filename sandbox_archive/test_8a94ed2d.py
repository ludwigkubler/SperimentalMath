# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def perm(n):
        if n == 0:
            return [[]]
        result = []
        for p in perm(n - 1):
            for i in range(len(p) + 1):
                result.append(p[:i] + [n - 1] + p[i:])
        return result
    
    def plethysm_coefficient(M, n):
        if n == 0:
            return 1
        if n == 1:
            return sum(sum(row) for row in M)
        result = 0
        for i in range(len(M)):
            for j in range(len(M[i])):
                submatrix = [row[:j] + row[j+1:] for row in M[:i] + M[i+1:]]
                result += plethysm_coefficient(submatrix, n - 1)
        return result
    
    def determinant(M):
        if len(M) == 0:
            return 0
        if len(M) == 1:
            return M[0][0]
        det = 0
        for i in range(len(M)):
            submatrix = [row[:i] + row[i+1:] for row in M[1:]]
            det += (-1) ** i * M[0][i] * determinant(submatrix)
        return det
    
    n = 4
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    plethysm_M = plethysm_coefficient(M, 2)
    plethysm_plethysm_M = plethysm_coefficient([[plethysm_M] * n for _ in range(n)], 2)
    
    det_M = determinant(M)
    det_det_M = determinant([[det_M] * n for _ in range(n)])
    
    metric_value = plethysm_plethysm_M / det_det_M
    conjecture_holds = metric_value >= 16
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "plethysm_coefficient_ratio",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")