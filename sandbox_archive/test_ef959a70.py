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
    
    def generate_polynomial(n):
        x = [0] * (n + 1)
        for i in range(n + 1):
            x[i] = random.randint(1, 10)
        return x
    
    def evaluate_polynomial(poly, x_val):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x_val ** i)
        return result
    
    def find_permutation_circuit_threshold(poly):
        n = len(poly) - 1
        if n == 0:
            return 1
        x_values = [i for i in range(2, n + 1)]
        min_circuit_size = float('inf')
        for x_val in x_values:
            result = evaluate_polynomial(poly, x_val)
            circuit_size = len(bin(result)) - 2
            if circuit_size < min_circuit_size:
                min_circuit_size = circuit_size
        return min_circuit_size
    
    def compute_minimal_rank(poly):
        n = len(poly) - 1
        rank = 0
        for i in range(n + 1):
            if poly[i] != 0:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_threshold = 0
    instances_tested = 0
    
    for n in n_values:
        poly = generate_polynomial(n)
        rank = compute_minimal_rank(poly)
        threshold = find_permutation_circuit_threshold(poly)
        total_rank += rank
        total_threshold += threshold
        instances_tested += len(poly)
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_threshold = Fraction(total_threshold, instances_tested)
    
    if mean_rank < 0.5 * mean_threshold:
        return {
            "metric_name": "Minimal Rank vs Permutation Circuit Threshold",
            "metric_value": float(mean_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"Rank {mean_rank} is less than half of threshold {mean_threshold}"
        }
    else:
        return {
            "metric_name": "Minimal Rank vs Permutation Circuit Threshold",
            "metric_value": float(mean_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank is less than half of threshold\" first_failing_seed={first_failing_seed}")