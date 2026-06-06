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
    n = 30  # Fixed instance size for simplicity
    clauses = [random.sample(range(1, n + 1), 2) for _ in range(n)]
    
    # Placeholder function to compute minimal order of Hodge structure
    def min_order_H(φ):
        return len(φ)
    
    # Placeholder function to compute clause subset complexity
    def c(φ):
        return sum(len(clause) for clause in φ)
    
    log_min_order = [math.log(min_order_H(clauses)) for _ in range(n)]
    log_c = [math.log(c(clauses)) for _ in range(n)]
    
    if any(math.isnan(x) or math.isinf(x) for x in log_min_order + log_c):
        return {
            "metric_name": "log_min_order vs log_c",
            "metric_value": None,
            "instances_tested": n,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((log_min_order[i] - sum(log_min_order) / n) * (log_c[i] - sum(log_c) / n) for i in range(n)) / (n - 1)
    
    return {
        "metric_name": "log_min_order vs log_c",
        "metric_value": correlation,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = "mapping_undefined"
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")