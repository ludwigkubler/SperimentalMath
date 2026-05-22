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
    
    def tropical_polynomial(n):
        return [random.uniform(-1, 1) for _ in range(n)]
    
    def evaluate_polynomial(poly, x):
        return sum(a * x**i for i, a in enumerate(poly))
    
    def count_real_points(poly):
        n = len(poly)
        real_points = set()
        for i in range(1000):  # Sample points in [0, 1]
            x = random.uniform(0, 1)
            if evaluate_polynomial(poly, x) == 0:
                real_points.add(x)
        return len(real_points)
    
    def acc0_circuit(depth, size):
        if depth == 0:
            return random.choice([1, -1])
        elif depth == 1:
            return random.choice([1, -1]) * acc0_circuit(0, size // 2) + random.choice([1, -1]) * acc0_circuit(0, size // 2)
        else:
            return random.choice([1, -1]) * acc0_circuit(depth - 1, size // 2) + random.choice([1, -1]) * acc0_circuit(depth - 1, size // 2)
    
    def compute_threshold(depth, size):
        epsilon = 0.1
        return 2 ** (depth / 2 + epsilon * size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        poly = tropical_polynomial(n)
        for _ in range(5):  # Test with 5 different ACC⁰ circuits
            depth = random.randint(1, 5)
            size = random.randint(1, 10)
            circuit_value = acc0_circuit(depth, size)
            threshold = compute_threshold(depth, size)
            real_points = count_real_points(poly)
            results.append({
                "n": n,
                "depth": depth,
                "size": size,
                "circuit_value": circuit_value,
                "threshold": threshold,
                "real_points": real_points
            })
    
    total_real_points = sum(result["real_points"] for result in results)
    mean_real_points = total_real_points / len(results)
    support_fraction = sum(1 for result in results if result["real_points"] >= result["threshold"]) / len(results)
    
    return {
        "metric_name": "Mean Real Points",
        "metric_value": mean_real_points,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support_fraction < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction < 0.8")