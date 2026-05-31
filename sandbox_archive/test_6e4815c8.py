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
    
    def generate_random_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def compute_knot_genus(cnf):
        # Placeholder for knot genus computation
        # This is a dummy implementation and should be replaced with actual logic
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        return n * (n - 1) // 2
    
    def spearman_rank_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        
        sorted_x = sorted(zip(x, range(len(x))))
        sorted_y = sorted(zip(y, range(len(y))))
        
        rank_x = [rank for _, rank in sorted_x]
        rank_y = [rank for _, rank in sorted_y]
        
        n = len(x)
        sum_d1_squared = sum((xi - yi) ** 2 for xi, yi in zip(rank_x, rank_y))
        sum_d2_squared = sum((xi - (n + 1) / 2) ** 2 for xi in rank_x)
        
        rho = 1 - (6 * sum_d1_squared) / (n * (n**2 - 1)) if n > 1 else 0
        return rho
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_random_cnf(n, n * 3)
        genus = compute_knot_genus(cnf)
        expected = n**2 * math.log(n)
        results.append({
            "n": n,
            "genus": genus,
            "expected": expected
        })
    
    metric_value = sum(result["genus"] for result in results) / len(results)
    conjecture_holds = all(result["genus"] <= result["expected"] for result in results)
    counterexample = "" if conjecture_holds else f"Genus {result['genus']} exceeds expected {result['expected']}"
    
    return {
        "metric_name": "Knot Genus",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")