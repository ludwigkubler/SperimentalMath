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
    
    def count_satisfying_assignments(f, n):
        count = 0
        for i in range(2**n):
            if all(f[i >> j & 1] == (i >> (j + 1)) & 1 for j in range(n)):
                count += 1
        return count
    
    def shannon_entropy(count, total):
        if count == 0 or count == total:
            return 0
        p = count / total
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    g_n_values = []
    E_f_values = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            g_n = count_satisfying_assignments(f, n)
            if g_n == 0 or g_n == 2**n:
                continue
            instances_tested += 1
            E_f = shannon_entropy(g_n, 2**n)
            g_n_values.append(math.log(g_n))
            E_f_values.append(E_f)
    
    if not g_n_values or not E_f_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(g_n_values)
    sum_g_n = sum(g_n_values)
    sum_E_f = sum(E_f_values)
    sum_g_n_E_f = sum(g * e for g, e in zip(g_n_values, E_f_values))
    sum_g_n_squared = sum(g**2 for g in g_n_values)
    
    correlation_coefficient = (n * sum_g_n_E_f - sum_g_n * sum_E_f) / math.sqrt((n * sum_g_n_squared - sum_g_n**2) * (n * sum_E_f**2 - sum_E_f**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(v <= 4 for v in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
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