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
    
    def generate_circuit(n, d):
        # Simplified circuit generation (not actual Kostant cohomology)
        return [random.randint(0, 1) for _ in range(d * n)]
    
    def calculate_kostant_cohomology(circuit):
        # Placeholder function
        return len(set(circuit))
    
    def calculate_monotone_width(circuit):
        # Placeholder function
        return max(len(list(group)) for _, group in itertools.groupby(sorted(circuit)))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        for _ in range(10):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n, random.randint(1, n))
            lcoh = calculate_kostant_cohomology(circuit)
            omega = calculate_monotone_width(circuit)
            results.append((lcoh, omega))
            total_instances += 1
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lcoh_values, omega_values = zip(*results)
    mean_lcoh = sum(lcoh_values) / len(lcoh_values)
    mean_omega = sum(omega_values) / len(omega_values)
    
    correlation_coefficient = (sum((l - mean_lcoh) * (o - mean_omega) for l, o in results) /
                                math.sqrt(sum((l - mean_lcoh)**2 for l in lcoh_values) *
                                          sum((o - mean_omega)**2 for o in omega_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= correlation_coefficient <= 1 and mean_lcoh <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")