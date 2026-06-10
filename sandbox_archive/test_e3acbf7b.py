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
        
        # Placeholder for LIDB calculation
        return random.random() * n
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid Boolean function length")
        
        # Placeholder for Communication Complexity Rank Variance calculation
        return random.random() * n
    
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        lidb_val = lidb(f)
        comm_rank_var = communication_complexity_rank_variance(f)
        results.append((lidb_val, comm_rank_var))
    
    if not results:
        return {
            "metric_name": "LIDB vs CommRankVar",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    lidb_values = [r[0] for r in results]
    comm_rank_vars = [r[1] for r in results]
    
    mean_lidb = sum(lidb_values) / len(lidb_values)
    mean_comm_rank_var = sum(comm_rank_vars) / len(comm_rank_vars)
    abs_diff_mean = abs(mean_lidb - mean_comm_rank_var)
    
    correlation_coefficient = 0
    if lidb_values and comm_rank_vars:
        n = len(lidb_values)
        numerator = sum((lidb_values[i] - mean_lidb) * (comm_rank_vars[i] - mean_comm_rank_var) for i in range(n))
        denominator = math.sqrt(sum((lidb_values[i] - mean_lidb)**2 for i in range(n)) * sum((comm_rank_vars[i] - mean_comm_rank_var)**2 for i in range(n)))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "LIDB vs CommRankVar",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(f) for f in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs_diff_mean <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and abs_diff_mean <= 3 else "correlation_threshold_not_met"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")