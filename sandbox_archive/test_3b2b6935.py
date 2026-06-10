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
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n gates
        return [random.choice(['AND', 'OR', 'NOT']) for _ in range(n)]
    
    def compute_hodge_rank(circuit):
        # Placeholder function to compute the Hodge rank of a circuit
        # This is a dummy implementation and should be replaced with actual computation
        return len(circuit)
    
    def compute_rank_variance(circuit):
        # Placeholder function to compute the rank variance of a circuit
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    n_max = 0
    instances_tested = 0
    hde_values = []
    rank_variance_values = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        circuit = generate_circuit(n)
        hde_rank = compute_hodge_rank(circuit)
        rank_variance = compute_rank_variance(circuit)
        
        hde_values.append(hde_rank)
        rank_variance_values.append(rank_variance)
        instances_tested += 1
    
    if n_max < 16:
        return {
            "metric_name": "Hodge Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max too low"
        }
    
    correlation_coefficient = sum((hde - hde_mean) * (rv - rv_mean) for hde, rv in zip(hde_values, rank_variance_values)) / (instances_tested * math.sqrt(sum((hde - hde_mean) ** 2 for hde in hde_values)) * math.sqrt(sum((rv - rv_mean) ** 2 for rv in rank_variance_values)))
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7 and max(hde - rv for hde, rv in zip(hde_values, rank_variance_values)) <= math.pow(2, c),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")