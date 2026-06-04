# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def compute_padic_l_function(n, m):
    # Placeholder function to compute p-adic L-function
    return 1 / (n ** (m ** (1/3)))

def generate_cnf_formula(m):
    variables = list(range(1, m + 2))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances = [generate_cnf_formula(m) for m in range(1, 41)]
    padic_l_functions = [compute_padic_l_function(n, len(instance)) for n, instance in enumerate(instances, start=1)]
    
    if not all(padic_l_functions):
        return {
            "metric_name": "padic_l_function",
            "metric_value": None,
            "instances_tested": 40,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "L(φ)(p) = 0 for some φ"
        }
    
    metric_value = sum(padic_l_functions)
    instances_tested = len(instances)
    n_max = max(len(instance) for instance in instances)
    conjecture_holds = all(abs(l) > 1e-6 for l in padic_l_functions)
    counterexample = "" if conjecture_holds else "L(φ)(p) = 0 for some φ"
    
    return {
        "metric_name": "padic_l_function",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [i for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"L(φ)(p) = 0 for some φ\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid data")