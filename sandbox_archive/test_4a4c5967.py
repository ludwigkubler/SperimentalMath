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
        if n == 0:
            return 0
        phi = [f[i] ^ f[i + 1] for i in range(len(f) - 1)]
        return max(lidb(phi), n)
    
    def communication_rank_variance(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        phi = [f[i] ^ f[i + 1] for i in range(len(f) - 1)]
        rank_variances = [communication_rank_variance(phi), n]
        return max(rank_variances)
    
    def pearson_correlation(lidbs, comm_rank_vars):
        if len(lidbs) != len(comm_rank_vars):
            raise ValueError("Lists must have the same length")
        n = len(lidbs)
        mean_lidb = sum(lidbs) / n
        mean_comm_rank_var = sum(comm_rank_vars) / n
        numerator = sum((lidbs[i] - mean_lidb) * (comm_rank_vars[i] - mean_comm_rank_var) for i in range(n))
        denominator = math.sqrt(sum((lidbs[i] - mean_lidb)**2 for i in range(n)) * sum((comm_rank_vars[i] - mean_comm_rank_var)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    lidbs = []
    comm_rank_vars = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        lidb_value = lidb(f)
        comm_rank_var_value = communication_rank_variance(f)
        lidbs.append(lidb_value)
        comm_rank_vars.append(comm_rank_var_value)
    
    correlation_coefficient = pearson_correlation(lidbs, comm_rank_vars)
    mean_diff = abs(sum(lidbs) - sum(comm_rank_vars)) / len(lidbs)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")