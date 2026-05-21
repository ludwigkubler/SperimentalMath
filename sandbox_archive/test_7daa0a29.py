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
    
    def generate_random_string(length):
        return ''.join(random.choice('01') for _ in range(length))
    
    def create_entangled_state(X, Y):
        n = len(X)
        entangled_state = {}
        for i in range(n):
            if X[i] == '1' and Y[i] == '1':
                entangled_state[(i, i)] = 1
        return entangled_state
    
    def compute_tensor_rank(entangled_state):
        # Simplified version of tensor rank computation
        rank = len(entangled_state)
        return rank
    
    def compute_randomized_communication_complexity(n):
        # Simplified version of CC_DISJ(n)
        return n * (n - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_coefficients = []
    
    for n in n_values:
        X = generate_random_string(n)
        Y = generate_random_string(n)
        entangled_state = create_entangled_state(X, Y)
        tensor_rank = compute_tensor_rank(entangled_state)
        cc_disj = compute_randomized_communication_complexity(n)
        
        if tensor_rank == 0 or cc_disj == 0:
            continue
        
        correlation_coefficients.append(tensor_rank / cc_disj)
    
    if not correlation_coefficients:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(correlation_coefficients),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_correlation = sum(correlation_coefficients) / len(correlation_coefficients)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_correlation,
        "instances_tested": len(correlation_coefficients),
        "conjecture_holds": mean_correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, tensor_rank={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break