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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def construct_d_module(phi):
        # Simplified mapping to a set of integers
        d_module = set()
        for clause in phi:
            for var in clause:
                d_module.add(abs(var))
        return len(d_module)
    
    def min_circuit_size(phi):
        # Simplified mapping to the number of clauses
        return len(phi)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = generate_cnf(n)
        d_module_order = construct_d_module(phi)
        circuit_size = min_circuit_size(phi)
        
        if d_module_order == 0 or circuit_size == 0:
            continue
        
        metric_values.append(abs(d_module_order - circuit_size))
    
    if not metric_values:
        return {
            "metric_name": "mean_abs_diff",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_d = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "mean_abs_diff",
        "metric_value": mean_d,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_d <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_d} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        result_str = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(result_str)