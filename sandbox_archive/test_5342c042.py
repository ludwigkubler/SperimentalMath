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

def generate_read_twice_bp(n):
    bp = []
    for _ in range(2**n):
        path = [random.choice([0, 1]) for _ in range(n)]
        bp.append(path)
    return bp

def count_paths(bp, i, j):
    count = 0
    for path in bp:
        if path[i] == j and path[j] == j:
            count += 1
    return count

def generate_transition_matrix(bp, n):
    M_P = [[count_paths(bp, i, j) for j in range(2)] for i in range(n)]
    return M_P

def r_transform(M, samples=1000):
    n = len(M)
    R = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for _ in range(samples):
                x = random.uniform(0, 1)
                y = random.uniform(0, 1)
                if M[i][j] > 0:
                    R[i][j] += (x - 1) / M[i][j]
    return R

def free_entropy(R):
    n = len(R)
    trace = sum(R[i][i] for i in range(n))
    det = 1
    for i in range(n):
        det *= R[i][i]
    return trace - math.log(det)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_read_twice_bp(n)
        M_P = generate_transition_matrix(bp, n)
        R = r_transform(M_P)
        φ_M_P = free_entropy(R)
        
        size_P = len(bp)
        conjecture_holds = φ_M_P <= math.log(size_P) + 5 * math.sqrt(n)
        counterexample = "" if conjecture_holds else "n={}".format(n)
        
        results.append({
            "metric_name": "free_entropy",
            "metric_value": φ_M_P,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", result)
        all_results.extend(result["results"])
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"n={}\" first_failing_seed={}".format(first_failing_seed, first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE insufficient data")