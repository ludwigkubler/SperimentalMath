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
    
    def generate_circuit(n):
        stack = []
        for _ in range(n):
            if random.choice([True, False]):
                stack.append(1)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        return stack[0]
    
    def calculate_entropy_variance(counts):
        mean = sum(counts) / len(counts)
        variance = sum((x - mean) ** 2 for x in counts) / len(counts)
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    all_counts = []
    
    for n in n_values:
        counts = [generate_circuit(n) for _ in range(30)]
        all_counts.extend(counts)
    
    variance = calculate_entropy_variance(all_counts)
    mean = sum(all_counts) / len(all_counts)
    support_fraction = 1.0
    
    conjecture_holds = mean <= n_values[-1] ** 2 and variance <= 0.1 * n_values[-1] ** 2
    counterexample = "" if conjecture_holds else "variance_too_high"
    
    return {
        "metric_name": "Entropy Variance",
        "metric_value": variance,
        "instances_tested": len(all_counts),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    std_variance = math.sqrt(sum((r["metric_value"] - mean_variance) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"variance_too_high\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE"
    
    print(result)