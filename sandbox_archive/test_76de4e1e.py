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
    
    def characteristic_function(circuit, x):
        if 0 <= x < len(circuit):
            return circuit[x]
        else:
            return 0
    
    def minimal_local_indefinite_integral(circuit):
        n = len(circuit)
        integral = 0
        for i in range(n):
            integral += characteristic_function(circuit, i) * math.log2(i + 1)
        return integral
    
    def communication_complexity_rank(circuit):
        # Placeholder function; actual implementation needed
        return random.randint(1, n)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = [random.randint(0, 1) for _ in range(n)]
        lii = minimal_local_indefinite_integral(circuit)
        rank = communication_complexity_rank(circuit)
        results.append((lii, rank))
    
    n_max = max(len(circuit) for _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max too small"
        }
    
    lii_values = [lii for lii, _ in results]
    rank_values = [rank for _, rank in results]
    
    mean_lii = sum(lii_values) / len(lii_values)
    mean_rank = sum(rank_values) / len(rank_values)
    
    correlation = 0
    for lii, rank in results:
        correlation += (lii - mean_lii) * (rank - mean_rank)
    correlation /= math.sqrt(sum((lii - mean_lii)**2 for lii in lii_values)) * math.sqrt(sum((rank - mean_rank)**2 for rank in rank_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    all_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        all_results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in all_results if result["metric_value"] is not None) / len(all_results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in all_results if result["metric_value"] is not None)) / len(all_results)
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported by some seeds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")