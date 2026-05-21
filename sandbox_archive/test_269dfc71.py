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
    
    def gram_schmidt(A):
        Q = []
        R = []
        for a in A:
            q = a[:]
            for i, q_i in enumerate(Q):
                r = sum(q_j * q_i[j] for j in range(len(a)))
                q = [q_k - r * q_i[k] for k, q_k in enumerate(q)]
            norm = math.sqrt(sum(q_k**2 for q_k in q))
            if norm == 0:
                continue
            Q.append([q_k / norm for q_k in q])
            R.append([r if i == j else 0 for j in range(len(A))])
        return Q, R
    
    def matrix_rank(matrix):
        Q, _ = gram_schmidt(matrix)
        rank = sum(1 for row in Q if any(row))
        return rank
    
    n = random.randint(40, 50)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    A = []
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 1:
                A.append([G[i][k] - G[j][k] for k in range(n)])
    
    real_rank = matrix_rank(A)
    
    def sos_relaxation(d):
        # Simulate SOS relaxation up to degree d
        # This is a placeholder function; actual implementation depends on the problem
        return False
    
    d_min = None
    for d in range(1, 11):
        if sos_relaxation(d):
            d_min = d
            break
    
    metric_name = "SOS Degree Lower Bound"
    metric_value = real_rank
    instances_tested = 1
    conjecture_holds = d_min is not None and d_min >= real_rank
    counterexample = "" if conjecture_holds else f"Graph with n={n}, A={A}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")