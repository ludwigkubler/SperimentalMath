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
    
    n = 40
    M = [[1 if i & j == 0 else 0 for j in range(n)] for i in range(n)]
    
    def singular_values(matrix):
        eigenvalues = []
        A = matrix
        B = [[0] * n for _ in range(n)]
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        for _ in range(20):  # Power iteration method to approximate singular values
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x * x for x in v))
            Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            Av_norm = math.sqrt(sum(x * x for x in Av))
            v = Av
            B = [[A[i][k] * v[k] / Av_norm for k in range(n)] for i in range(n)]
        
        eigenvalues.append(max(abs(sum(B[i][j] * v[j] for j in range(n))) for i in range(n)))
        return eigenvalues
    
    def noncommutative_lp_norm(eigenvalues, p):
        if p == 2:
            return max(eigenvalues)
        else:
            return (sum(x**(p/(p-1)) for x in eigenvalues))**(1/(p-1))
    
    min_p_norm = float('inf')
    for p in [1.5, 2, 2.5]:
        norm = noncommutative_lp_norm(singular_values(M), p)
        if norm < min_p_norm:
            min_p_norm = norm
    
    metric_value = min_p_norm
    conjecture_holds = metric_value >= 0.1 * math.sqrt(n)
    counterexample = "" if conjecture_holds else f"min_p_norm={min_p_norm}, n={n}"
    
    return {
        "metric_name": "Noncommutative L^p norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_p_norm < 0.1√n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")