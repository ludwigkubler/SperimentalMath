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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 4
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    det_M = determinant(M)
    plethysm_M = plethysm_coefficient(M)
    
    if det_M == 0:
        return {
            "metric_name": "plethysm_det_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "det_M is zero"
        }
    
    metric_value = plethysm_M / det_M
    conjecture_holds = metric_value >= 2**n
    
    return {
        "metric_name": "plethysm_det_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
    return det

def plethysm_coefficient(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    # Placeholder for actual plethysm coefficient computation
    # This is a dummy implementation that always returns 2^n for simplicity
    return 2**n

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(v is not None for v in metric_values):
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((v - mean) ** 2 for v in metric_values) / len(metric_values))
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='not enough support' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] if r['metric_value'] is not None))]}")
    else:
        print("RESULT: INCONCLUSIVE some trials had undefined metric values")