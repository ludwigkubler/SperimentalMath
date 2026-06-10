# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def algebraic_cycle_representation(circuit):
        n = len(circuit) ** 0.5
        if not n.is_integer():
            return None
        n = int(n)
        if all(sum(circuit[i:i+n] == circuit[j:j+n] for i, j in combinations(range(2**n), n)) for _ in range(n)):
            return n
        else:
            return None
    
    def rank_variance(circuit):
        # Placeholder function; replace with actual calculation
        return random.random()
    
    alpha_C_values = []
    rank_variance_values = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_circuit(n)
        alpha_C = algebraic_cycle_representation(circuit)
        if alpha_C is not None:
            alpha_C_values.append(alpha_C)
            rank_variance_values.append(rank_variance(circuit))
    
    if not alpha_C_values or not rank_variance_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": len(alpha_C_values),
            "n_max": max(n for n in range(5, 41) if any(len(circuit) == n**2 for circuit in [generate_circuit(n)])),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_alpha_C = sum(alpha_C_values) / len(alpha_C_values)
    mean_rank_variance = sum(rank_variance_values) / len(rank_variance_values)
    
    covariance = sum((alpha_C - mean_alpha_C) * (rank_variance - mean_rank_variance) for alpha_C, rank_variance in zip(alpha_C_values, rank_variance_values)) / len(alpha_C_values)
    variance_alpha_C = sum((alpha_C - mean_alpha_C)**2 for alpha_C in alpha_C_values) / len(alpha_C_values)
    variance_rank_variance = sum((rank_variance - mean_rank_variance)**2 for rank_variance in rank_variance_values) / len(rank_variance_values)
    
    pearson_corr_coeff = covariance / (variance_alpha_C ** 0.5 * variance_rank_variance ** 0.5)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(alpha_C_values),
        "n_max": max(n for n in range(5, 41) if any(len(circuit) == n**2 for circuit in [generate_circuit(n)])),
        "conjecture_holds": pearson_corr_coeff >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")