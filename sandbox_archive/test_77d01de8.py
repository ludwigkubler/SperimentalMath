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
    
    def tree_like_resolution_width(f):
        n = len(f)
        if n == 1:
            return 1
        minterms = set()
        for i in range(2**n):
            minterm = [f[i >> j & 1] for j in range(n)]
            minterms.add(tuple(minterm))
        return max(len(list(g)) for _, g in groupby(sorted(minterms), key=lambda x: x[:-1]))
    
    def symplectic_leaf_system(f):
        n = len(f)
        leaves = set()
        for i in range(2**n):
            minterm = [f[i >> j & 1] for j in range(n)]
            if all(minterm[j] == f[i >> (j+1) & 1] for j in range(n-1)):
                leaves.add(tuple(minterm))
        return leaves
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        w_t_f = tree_like_resolution_width(f)
        L_f = symplectic_leaf_system(f)
        results.append({
            "n": n,
            "w_t_f": w_t_f,
            "L_f": len(L_f),
            "instances_tested": 1
        })
    
    if not results:
        return {
            "metric_name": "symplectic_leaves_number",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["L_f"] for r in results]
    w_t_f_squared = [r["w_t_f"]**2 for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    
    if len(metric_values) < 30:
        return {
            "metric_name": "symplectic_leaves_number",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    
    correlation_sum = 0
    for i in range(len(metric_values)):
        correlation_sum += (metric_values[i] - mean_metric) * (w_t_f_squared[i] - sum(w_t_f_squared) / len(w_t_f_squared))
    correlation = correlation_sum / (len(metric_values) * std_metric * math.sqrt(sum((x - sum(w_t_f_squared) / len(w_t_f_squared))**2 for x in w_t_f_squared)))
    
    return {
        "metric_name": "symplectic_leaves_number",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation > 0.7 and correlation < 1.0,
        "counterexample": "" if correlation > 0.7 else f"correlation={correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric:.2f} std={std_metric:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"] != "")
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_samples")