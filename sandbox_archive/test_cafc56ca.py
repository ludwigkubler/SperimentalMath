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
    n = 40
    random.seed(seed)
    
    def generate_transition_matrix():
        return [[random.random() for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
        return result
    
    def r_transform(P):
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        P_inv = [row[:] for row in P]
        for _ in range(1, n):
            P_inv = matrix_multiply(P_inv, P)
        R = [[P[i][j] - I[i][j] for j in range(n)] for i in range(n)]
        return R
    
    def operator_norm(R):
        max_eigenvalue = 0
        for _ in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
            Rv = matrix_multiply(R, v)
            max_eigenvalue = max(max_eigenvalue, abs(v[0] * Rv[0][0]))
        return max_eigenvalue
    
    # Generate IP_2's read-twice BP
    P_ip2 = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    P_ip2[0][1], P_ip2[1][0] = 1, 1
    R_ip2 = r_transform(P_ip2)
    norm_ip2 = operator_norm(R_ip2)
    
    # Generate 30 random read-twice BPs
    results = []
    for _ in range(30):
        P_random = generate_transition_matrix()
        R_random = r_transform(P_random)
        norm_random = operator_norm(R_random)
        
        if norm_random > 1.2 * math.log(n):
            counterexample = "Random BP with high norm"
            return {
                "metric_name": "Operator Norm",
                "metric_value": norm_random,
                "instances_tested": 30,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append(norm_random)
    
    if norm_ip2 < 0.9 * n:
        counterexample = "IP_2 BP with low norm"
        return {
            "metric_name": "Operator Norm",
            "metric_value": norm_ip2,
            "instances_tested": 30,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "Operator Norm",
        "metric_value": norm_ip2,
        "instances_tested": 30,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.9 * n) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < 0.9 * n)]
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 BP with low norm\" first_failing_seed={first_failing_seed}")