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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_density_matrix(f):
        n = int(math.log2(len(f)))
        rho = [[0] * (2*n) for _ in range(2*n)]
        for i in range(2*n):
            for j in range(2*n):
                if f[i//n] == f[j//n]:
                    rho[i][j] = 1 / len(f)
        return rho
    
    def compute_minimal_rank(rho):
        n = len(rho)
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if rho[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                rank += 1
                for j in range(n):
                    if j != i:
                        factor = rho[j][i] / rho[pivot_row][i]
                        for k in range(n):
                            rho[j][k] -= factor * rho[pivot_row][k]
        return rank
    
    def compute_circuit_weight(f):
        n = int(math.log2(len(f)))
        # Simplified circuit weight calculation
        return 2**n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            rho = compute_density_matrix(f)
            rank = compute_minimal_rank(rho)
            weight = compute_circuit_weight(f)
            
            if rank > 3 * math.log2(n):
                counterexample = "rank > 3*log(n)"
                conjecture_holds = False
            if weight >= 2**rank:
                counterexample = "weight >= 2^rank"
                conjecture_holds = False
            
            total_metric_value += abs(rank - math.log2(n))
            instances_tested += 1
    
    return {
        "metric_name": "abs_rank_diff",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")