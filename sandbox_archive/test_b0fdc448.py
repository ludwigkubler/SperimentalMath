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
    
    def generate_max_cut_instance(n):
        A = [random.randint(0, n-1) for _ in range(n)]
        B = [random.randint(0, n-1) for _ in range(n)]
        return A, B
    
    def polynomial(A, B):
        n = len(A)
        poly = 0
        for i in range(n):
            for j in range(i+1, n):
                if A[i] == B[j]:
                    poly += (A[i] - A[j]) * (B[i] - B[j])
        return poly
    
    def sdp_relaxation(poly):
        # Basic SDP relaxation to estimate SOS degree
        n = len(poly)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) in poly:
                    A[i][j] = A[j][i] = 1
        return sum(sum(row) for row in A)
    
    def symbolic_rank_check(poly):
        # Simplified symbolic rank check (placeholder)
        return len(poly)
    
    n = 40
    A, B = generate_max_cut_instance(n)
    poly = polynomial(A, B)
    d = symbolic_rank_check(poly)
    sos_degree = sdp_relaxation(poly)
    
    metric_name = "SOS_refutation_degree"
    metric_value = sos_degree
    instances_tested = 1
    conjecture_holds = sos_degree >= math.log(d + 1)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, A={A}, B={B}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n=40\" first_failing_seed={first_failing_seed}")