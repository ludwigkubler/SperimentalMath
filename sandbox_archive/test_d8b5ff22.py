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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_communication = 0
        for i in range(2**n):
            comm = sum(f[i >> j & 1] for j in range(n))
            if comm > max_communication:
                max_communication = comm
        return max_communication
    
    def algebraic_k_group_rank(f):
        n = len(f)
        # Simplified rank calculation based on the number of 1s in the function
        return sum(1 for x in f if x == 1)
    
    def log_growth_rate(rank, instances):
        if instances <= 0:
            return 0
        return math.log(rank) / math.log(instances)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_random_boolean_function(n)
            rank = algebraic_k_group_rank(f)
            comm_rank = communication_complexity(f)
            log_growth = log_growth_rate(rank, len(results) + 1)
            results.append((log_growth, comm_rank))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_growth = [r[0] for r in results]
    comm_rank = [r[1] for r in results]
    n = len(log_growth)
    
    # Calculate correlation coefficient
    mean_log_growth = sum(log_growth) / n
    mean_comm_rank = sum(comm_rank) / n
    cov = sum((log_growth[i] - mean_log_growth) * (comm_rank[i] - mean_comm_rank) for i in range(n)) / n
    var_log_growth = sum((log_growth[i] - mean_log_growth)**2 for i in range(n)) / n
    var_comm_rank = sum((comm_rank[i] - mean_comm_rank)**2 for i in range(n)) / n
    correlation_coefficient = cov / math.sqrt(var_log_growth * var_comm_rank)
    
    # Calculate slope of the linear regression line
    slope = cov / var_log_growth
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(slope) <= 3 * math.sqrt(var_comm_rank / var_log_growth),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")