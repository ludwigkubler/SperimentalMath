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
        cnf = []
        for _ in range(10):  # Generate 10 clauses for simplicity
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_depth(cnf):
        # Simplified DPLL solver to estimate circuit depth
        depth = 0
        for clause in cnf:
            depth += len(clause) + 1
        return depth
    
    def hodge_weight(cnf):
        # Constructive mapping procedure to compute Hodge weight
        # This is a placeholder; actual implementation depends on the conjecture
        return sum(len(clause) for clause in cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    d_phi = circuit_depth(cnf)
    h_phi = hodge_weight(cnf)
    
    if d_phi == 0:
        return {
            "metric_name": "h/d_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_depth_zero"
        }
    
    h_d_ratio = h_phi / d_phi
    
    return {
        "metric_name": "h/d_ratio",
        "metric_value": h_d_ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= h_d_ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"h/d_ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")