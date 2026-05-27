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
    
    def geometric_entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def generate_monotone_circuit(n, depth):
        if depth == 1:
            return random.choice([0, 1])
        else:
            left = generate_monotone_circuit(n // 2, depth - 1)
            right = generate_monotone_circuit(n - n // 2, depth - 1)
            return max(left, right) if random.choice([0, 1]) == 0 else min(left, right)

    def compute_geometric_entropy(circuit):
        counts = [0] * 2
        for _ in range(1000):  # Sample 1000 inputs
            input_val = generate_monotone_circuit(n, depth)
            output_val = circuit(input_val)
            counts[output_val] += 1
        p0 = counts[0] / sum(counts)
        p1 = counts[1] / sum(counts)
        return geometric_entropy(p0) + geometric_entropy(p1)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        depth = random.randint(1, int(math.log2(n)) + 1)
        circuit = generate_monotone_circuit(n, depth)
        entropy = compute_geometric_entropy(circuit)
        results.append({
            "n": n,
            "depth": depth,
            "entropy": entropy
        })
    
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    support_fraction = all(entropy >= (result["n"] ** 0.25) / result["depth"] for result in results)
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")