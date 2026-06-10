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
    
    def generate_circuit(size):
        # Simplified circuit generation (e.g., AND gates)
        return [random.choice([0, 1]) for _ in range(2 ** size)]
    
    def hodge_decomposition(circuit):
        # Placeholder Hodge decomposition
        return len(circuit) // 2
    
    def rank_variance(circuit):
        # Placeholder rank variance calculation
        return sum(abs(x - y) for x, y in zip(circuit[:-1], circuit[1:])) / (len(circuit) - 1)
    
    hde_values = []
    rank_variance_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_circuit(n)
            hde = hodge_decomposition(circuit)
            rv = rank_variance(circuit)
            
            hde_values.append(hde)
            rank_variance_values.append(rv)
            instances_tested += 1
    
    if not hde_values or not rank_variance_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    hde_mean = sum(hde_values) / len(hde_values)
    rv_mean = sum(rank_variance_values) / len(rank_variance_values)
    
    correlation_coefficient = sum((hde - hde_mean) * (rv - rv_mean) for hde, rv in zip(hde_values, rank_variance_values)) / (instances_tested * math.sqrt(sum((hde - hde_mean) ** 2 for hde in hde_values)) * math.sqrt(sum((rv - rv_mean) ** 2 for rv in rank_variance_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")