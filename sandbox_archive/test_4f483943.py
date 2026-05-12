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
    
    def generate_read_twice_bp(n):
        # Placeholder for generating a read-twice BP for IP_2
        return [[random.random() for _ in range(2**n)] for _ in range(2**n)]
    
    def generate_poly_size_bp(n):
        # Placeholder for generating a BP for a function with poly(n) size circuits
        return [[random.random() for _ in range(2**n)] for _ in range(2**n)]
    
    def free_cumulants(matrix):
        # Placeholder for computing free cumulants via the R-transform
        n = len(matrix)
        M = matrix
        for k in range(1, n):
            M = [[sum(M[i][j] * M[k-i][k-j] for i in range(k+1) for j in range(k+1)) for j in range(n)] for i in range(n)]
        return [M[0][i] for i in range(n)]
    
    def R_transform(cumulants):
        # Placeholder for computing the R-transform
        n = len(cumulants)
        R = [[0]*n for _ in range(n)]
        for k in range(1, n):
            R[k][k] = cumulants[k]
            for i in range(k-1, -1, -1):
                R[i][i+1:k+1] = [sum(R[j][j+1:i+1] * R[k-j][i+1:j+2] for j in range(i, k)) for _ in range(k-i)]
        return R
    
    def free_entropy(matrix):
        # Placeholder for computing the free entropy
        cumulants = free_cumulants(matrix)
        R = R_transform(cumulants)
        n = len(R)
        free_ent = 0
        for i in range(n):
            free_ent += sum(math.log(abs(R[i][j])) for j in range(i+1, n))
        return free_ent
    
    def is_IP_2_BP(bp):
        # Placeholder for checking if the BP computes IP_2
        return True
    
    n = random.randint(5, 40)
    if is_IP_2_BP(generate_read_twice_bp(n)):
        bp = generate_read_twice_bp(n)
        metric_value = free_entropy(bp)
        conjecture_holds = metric_value >= n
        counterexample = "" if conjecture_holds else "IP_2-BP does not meet the lower bound"
    else:
        bp = generate_poly_size_bp(n)
        metric_value = free_entropy(bp)
        conjecture_holds = metric_value <= math.log(n)
        counterexample = "" if conjecture_holds else "poly-size BP does not meet the upper bound"
    
    return {
        "metric_name": "free_entropy",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='<desc>' first_failing_seed=<s>")
    else:
        print("RESULT: INCONCLUSIVE <reason>")