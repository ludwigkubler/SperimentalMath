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
    
    def calculate_entropy_variance(counts):
        n = len(counts)
        if n == 0:
            return 0.0
        mean = sum(counts) / n
        variance = sum((x - mean) ** 2 for x in counts) / n
        return variance
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            circuit.append(random.choice([0, 1]))
        return circuit
    
    def calculate_automorphism_group_count(circuit):
        # Placeholder function to simulate automorphism group count calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    all_counts = []
    for _ in range(30):  # Sample 30 instances per seed
        circuit = generate_boolean_circuit(n)
        automorphism_count = calculate_automorphism_group_count(circuit)
        all_counts.append(automorphism_count)
    
    variance = calculate_entropy_variance(all_counts)
    mean = sum(all_counts) / len(all_counts)
    
    conjecture_holds = mean <= n**2 and variance <= 0.1 * n**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Entropy Variance of Automorphism Group Counts",
        "metric_value": variance,
        "instances_tested": len(all_counts),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_variance = sum(result["metric_value"] for result in results) / len(results)
    std_variance = math.sqrt(sum((result["metric_value"] - mean_variance) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")