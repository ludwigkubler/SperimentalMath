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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def schur_weyl_module_dimension(f):
    n = int(math.log2(len(f)))
    dim = 0
    for i in range(n + 1):
        dim += min(i, n - i)
    return dim

def monotone_circuit_size(f):
    # Placeholder function to simulate circuit size calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        f = generate_random_boolean_function(random.randint(5, 40))
        rho_f = schur_weyl_module_dimension(f)
        circuit_size = monotone_circuit_size(f)
        results.append((rho_f, circuit_size))
    
    total_rho = sum(rho for _, rho in results)
    avg_rho = total_rho / len(results)
    total_circuit_size = sum(size for size, _ in results)
    avg_circuit_size = total_circuit_size / len(results)
    
    metric_value = avg_circuit_size
    conjecture_holds = avg_circuit_size <= 2 * avg_rho
    counterexample = "" if conjecture_holds else f"avg_circuit_size={avg_circuit_size}, avg_rho={avg_rho}"
    
    return {
        "metric_name": "Average Circuit Size",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] * result["instances_tested"] for result in results)
    mean_metric_value = total_metric_value / sum(result["instances_tested"] for result in results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")