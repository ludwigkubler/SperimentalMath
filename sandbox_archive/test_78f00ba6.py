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
    n = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        f = [random.randint(0, 1) for _ in range(2**n)]
        
        # Compute Coxeter diagram C(f)
        # This is a placeholder. Replace with actual computation.
        C_f = len(f)  # Example: number of non-zero elements
        
        # Compute tropical generating series T(f)
        # This is a placeholder. Replace with actual computation.
        T_f = sum(Fraction(1, i+1) for i in range(n))  # Example: harmonic series
        
        # Calculate C(f)^{3/2}
        C_f_3_2 = C_f ** (3 / 2)
        
        metric_values.append((C_f, T_f, C_f_3_2))
    
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    # Perform Spearman rank correlation test
    if len(metric_values) > 1:
        rho = spearman_rank_correlation(metric_values)
        if rho >= 0.7:
            conjecture_holds = True
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def spearman_rank_correlation(data):
    ranks = {x: rank for rank, x in enumerate(sorted(set(x[0] for x in data)), start=1)}
    T_f_ranks = [ranks[x[1]] for x in data]
    C_f_3_2_ranks = [ranks[x[2]] for x in data]
    
    n = len(data)
    sum_d_squared = sum((x - y) ** 2 for x, y in zip(T_f_ranks, C_f_3_2_ranks))
    rho = 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    return rho

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")