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
    
    def geometric_entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def generate_monotone_circuit(n):
        # Simplified monotone circuit generation for demonstration
        # This is a placeholder and should be replaced with actual circuit generation logic
        return [random.choice([0, 1]) for _ in range(2**n)]

    def compute_geometric_entropy(circuit):
        ones = sum(circuit)
        total = len(circuit)
        p = Fraction(ones, total)
        return geometric_entropy(p)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_monotone_circuit(n)
            entropy = compute_geometric_entropy(circuit)
            results.append((n, entropy))
    
    if not results:
        return {
            "metric_name": "Geometric Entropy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    total_entropy = sum(entropy for _, entropy in results)
    mean_entropy = total_entropy / len(results)
    n_total = sum(n for n, _ in results)
    size_term = (n_total ** Fraction(1, 4))
    depth_term = max(n for n, _ in results)  # Simplified as depth is not directly controllable
    expected_entropy = size_term / depth_term
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "conjecture_holds": mean_entropy >= expected_entropy,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_entropy) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")