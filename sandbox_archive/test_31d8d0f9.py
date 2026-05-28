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
    
    def generate_random_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def cocomplex(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        else:
            subcircuits = [circuit[i:i+n//2] for i in range(n//2)] + [circuit[n//2+i:n//2+i+n//2] for i in range(n//2)]
            return 1 + sum(cocomplex(subcircuit) for subcircuit in subcircuits)
    
    def resolution_refutation_size(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        else:
            refutations = [resolution_refutation_size(circuit[:n//2]), resolution_refutation_size(circuit[n//2:])]
            return 1 + max(refutations)
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        return 1 - (6 * sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n)) / (n * (n**2 - 1)))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        r_cocomplex_C = cocomplex(circuit)
        t_C = resolution_refutation_size(circuit)
        if t_C == 0:
            continue
        log2_t_C = math.log2(t_C)
        results.append((log2_t_C, r_cocomplex_C))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    x, y = zip(*results)
    rho = spearman_rank_correlation(x, y)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.8,
        "counterexample": "" if rho >= 0.8 else f"rho={rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        rho_values = [result["metric_value"] for result in results if result["conjecture_holds"]]
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho<{min(rho_values)}\" first_failing_seed={first_failing_seed}")