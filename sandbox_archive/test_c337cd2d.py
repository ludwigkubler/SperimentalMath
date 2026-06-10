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
    
    def lidb(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid Boolean function length")
        
        def is_independent(x, y):
            return all(f[i] == f[j] for i in range(2**n) for j in range(i+1, 2**n) if (i & x) == (j & x) and (i & y) != (j & y))
        
        max_independent_set = []
        for i in range(n):
            independent_set = [1 << i]
            for j in range(n):
                if is_independent(i, j):
                    independent_set.append(1 << j)
            if len(independent_set) > len(max_independent_set):
                max_independent_set = independent_set
        
        return len(max_independent_set)
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid Boolean function length")
        
        def rank(f, x):
            count = [0] * (1 << n)
            for i in range(2**n):
                if f[i] == x:
                    count[i & ((1 << n) - 1)] += 1
            return max(count)
        
        r1 = rank(f, 0)
        r2 = rank(f, 1)
        return abs(r1 - r2)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        lidb_value = lidb(f)
        comm_rank_variance = communication_complexity_rank_variance(f)
        results.append((lidb_value, comm_rank_variance))
    
    if not results:
        return {
            "metric_name": "LIDB vs CommRankVar",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    lidb_values = [r[0] for r in results]
    comm_rank_variances = [r[1] for r in results]
    
    mean_lidb = sum(lidb_values) / len(lidb_values)
    mean_comm_rank_variance = sum(comm_rank_variances) / len(comm_rank_variances)
    abs_diff_mean = abs(mean_lidb - mean_comm_rank_variance)
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((lidb_values[i] - mean_lidb) * (comm_rank_variances[i] - mean_comm_rank_variance) for i in range(len(results)))
        denominator = math.sqrt(sum((lidb_values[i] - mean_lidb)**2 for i in range(len(results))) * sum((comm_rank_variances[i] - mean_comm_rank_variance)**2 for i in range(len(results))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "LIDB vs CommRankVar",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs_diff_mean <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and abs_diff_mean <= 3 else "correlation_too_low_or_abs_diff_too_high"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low_or_abs_diff_too_high\" first_failing_seed={first_failing_seed}")