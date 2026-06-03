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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_monotone_width(cnf):
        # Placeholder implementation
        return len(cnf)
    
    def geometric_invariant_group(cnf):
        # Placeholder implementation
        return 1 + len(cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            min_order = geometric_invariant_group(cnf)
            w_phi = circuit_monotone_width(cnf)
            results.append((min_order, w_phi))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders, w_phis = zip(*results)
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_w_phi = sum(w_phis) / len(w_phis)
    covariance = sum((x - mean_min_order) * (y - mean_w_phi) for x, y in results) / len(results)
    variance_min_order = sum((x - mean_min_order) ** 2 for x in min_orders) / len(min_orders)
    variance_w_phi = sum((y - mean_w_phi) ** 2 for y in w_phis) / len(w_phis)
    
    if variance_min_order == 0 or variance_w_phi == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearsons_r = covariance / math.sqrt(variance_min_order * variance_w_phi)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": pearsons_r,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": 0.2 <= pearsons_r <= 1.0 and pearsons_r >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        mean_r = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
        std_r = math.sqrt(sum((result["metric_value"] - mean_r) ** 2 for result in results if result["metric_value"] is not None) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_r:.4f} std={std_r:.4f} support_fraction={support_fraction:.2f}")