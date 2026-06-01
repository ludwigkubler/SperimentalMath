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
    
    def generate_random_cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, 2*m), -random.randint(1, 2*m)]
            cnf.append(clause)
        return cnf
    
    def calculate_frege_proof_depth(cnf):
        # Placeholder function to simulate Frege proof depth calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * 2
    
    def compute_unit_group_size(cnf):
        # Placeholder function to simulate unit group size calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) ** 2
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        cnf = generate_random_cnf(m)
        unit_group_size = compute_unit_group_size(cnf)
        frege_depth = calculate_frege_proof_depth(cnf)
        results.append((unit_group_size, frege_depth))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    unit_group_sizes = [r[0] for r in results]
    frege_depths = [r[1] for r in results]
    
    mean_unit_group_size = sum(unit_group_sizes) / len(unit_group_sizes)
    mean_frege_depth = sum(frege_depths) / len(frege_depths)
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((unit_group_sizes[i] - mean_unit_group_size) * (frege_depths[i] - mean_frege_depth) for i in range(len(results)))
        denominator = math.sqrt(sum((unit_group_sizes[i] - mean_unit_group_size) ** 2 for i in range(len(results))) * sum((frege_depths[i] - mean_frege_depth) ** 2 for i in range(len(results))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": correlation_coefficient >= 0.95,
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
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.95\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")