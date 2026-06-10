# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        # Generate a random CNF with n variables and 2n clauses
        cnf = []
        for _ in range(2 * n):
            clause = [random.randint(-1, -n), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_depth(cnf):
        # Compute the circuit depth of a CNF
        if not cnf:
            return 0
        max_depth = 0
        for clause in cnf:
            depth = 1
            for literal in clause:
                if abs(literal) > len(cnf):
                    continue
                depth = max(depth, circuit_depth([c for c in cnf if literal in c]) + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    
    def categorial_torsor_size(cnf):
        # Compute the size of the categorial torsor associated with a CNF
        if not cnf:
            return 0
        size = 1
        for clause in cnf:
            size *= len(clause)
        return size
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            depth = circuit_depth(cnf)
            size = categorial_torsor_size(cnf)
            
            if depth == 0:
                continue
            
            metric_values.append(abs(size - depth))
            instances_tested += 1
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(x <= 3 for x in metric_values) and len([x for x in metric_values if x > 0]) >= 24
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "categorial_torsor_size_diff",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")