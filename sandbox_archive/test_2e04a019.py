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
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def sample_satisfying_assignments(f, m):
        n = len(f)
        satisfying_assignments = []
        for assignment in product([0, 1], repeat=n):
            if f(assignment):
                satisfying_assignments.append(assignment)
                if len(satisfying_assignments) == m:
                    break
        return satisfying_assignments
    
    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))
    
    def greedy_ball_cover(f, S, R):
        covered = set()
        count = 0
        while len(covered) < len(S):
            max_points = []
            max_count = 0
            for c_j in S:
                if c_j not in covered:
                    points_in_range = [y for y in S if hamming_distance(c_j, y) <= R]
                    if len(points_in_range) > max_count:
                        max_points = points_in_range
                        max_count = len(points_in_range)
            if max_count == 0:
                break
            count += 1
            covered.update(max_points)
        return count
    
    def f(x):
        n = len(x)
        # Example function: OR of the first half of the bits
        return any(x[i] for i in range(n // 2))
    
    n_values = [6, 10, 16, 24, 32, 40]
    results = []
    total_instances_tested = 0
    
    for n in n_values:
        m = 64
        S = sample_satisfying_assignments(f, m)
        instances_tested = 0
        
        for _ in range(30):
            i = random.randint(0, n - 1)
            b = random.choice([0, 1])
            R = random.randint(1, n // 2)
            
            f_prime = lambda x: f(x[:i] + (b,) + x[i+1:])
            kappa_R_f = greedy_ball_cover(f, S, R)
            kappa_R_f_prime = greedy_ball_cover(f_prime, S, R)
            delta = abs(kappa_R_f - kappa_R_f_prime)
            
            instances_tested += 1
            total_instances_tested += 1
            
            results.append({
                "metric_name": "delta",
                "metric_value": delta,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": delta <= 2 * (len(n_values) + 1).bit_length(),
                "counterexample": ""
            })
    
    mean_delta = sum(result["metric_value"] for result in results) / len(results)
    std_delta = (sum((result["metric_value"] - mean_delta) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        return {
            "seed": seed,
            "metric_name": "delta",
            "mean_delta": mean_delta,
            "std_delta": std_delta,
            "support_fraction": support_fraction,
            "RESULT": f"SUPPORTED mean={mean_delta} std={std_delta} support_fraction={support_fraction}"
        }
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        return {
            "seed": seed,
            "metric_name": "delta",
            "mean_delta": mean_delta,
            "std_delta": std_delta,
            "support_fraction": support_fraction,
            "RESULT": f"FALSIFIED counterexample=\"delta_exceeds_threshold\" first_failing_seed={first_failing_seed}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")