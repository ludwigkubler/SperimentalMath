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
    
    def generate_affine_variety(n):
        # Generate a random affine variety over F_2 with n variables
        return [random.choice(['x', '1']) for _ in range(n)]
    
    def compute_minimal_local_ring_norm(V):
        # Compute the minimal local ring norm of V (simplified example)
        return len(set(V)) / len(V) if V else 0
    
    def construct_frege_proof_length(V):
        # Construct a Frege proof length for V (simplified example)
        return len(V) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    mrl_values = []
    f_values = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            V = generate_affine_variety(n)
            mrl = compute_minimal_local_ring_norm(V)
            f = construct_frege_proof_length(V)
            mrl_values.append(mrl)
            f_values.append(f)
    
    if not mrl_values or not f_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_variety"
        }
    
    mean_mrl = sum(mrl_values) / len(mrl_values)
    mean_f = sum(f_values) / len(f_values)
    
    correlation_coefficient = sum((mrl - mean_mrl) * (f - mean_f) for mrl, f in zip(mrl_values, f_values)) / math.sqrt(sum((mrl - mean_mrl) ** 2 for mrl in mrl_values) * sum((f - mean_f) ** 2 for f in f_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mrl_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) >= 2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")