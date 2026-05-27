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
    
    def generate_boolean_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def free_entropy(matrix):
        n = len(matrix)
        trace_sum = sum(sum(row[i] * row[j] for j in range(n)) for i in range(n))
        return -trace_sum / (n ** 2)
    
    def communication_complexity(matrix):
        # Simplified version of CC_R for disjointness problem
        n = len(matrix)
        count = sum(1 for row in matrix if sum(row) == 1)
        return math.log2(count + 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = generate_boolean_matrix(n)
        F_star_M = free_entropy(M)
        CC_R_DISJ_n = communication_complexity(M)
        
        if F_star_M == 0 or CC_R_DISJ_n == 0:
            continue
        
        results.append((F_star_M, CC_R_DISJ_n))
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    F_star_values = [F for F, _ in results]
    CC_R_values = [CC for _, CC in results]
    
    n = len(F_star_values)
    rank_F_star = sorted(range(n), key=lambda i: F_star_values[i])
    rank_CC_R = sorted(range(n), key=lambda i: CC_R_values[i])
    
    rho = sum((rank_F_star[i] - (n + 1) / 2) * (rank_CC_R[i] - (n + 1) / 2) for i in range(n)) / (n * (n**2 - 1))
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": n,
        "conjecture_holds": abs(rho) >= 0.6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation below threshold\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE Some trials did not produce a valid metric value")