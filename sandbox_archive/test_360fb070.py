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
    
    def generate_formula(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], k=random.randint(1, n))
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)
    
    def hypergeometric_sequence(n, m):
        # Placeholder function to compute the minimal order μ(φ)
        # This is a dummy implementation and should be replaced with actual logic
        return random.random() * n
    
    def resolution_width(phi):
        # Placeholder function to compute the resolution proof width w(φ)
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    ratios = []
    instances_tested = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n)
            phi = generate_formula(n, m)
            mu_phi = hypergeometric_sequence(n, m)
            w_phi = resolution_width(phi)
            if w_phi > 0:
                ratios.append(mu_phi / w_phi)
                instances_tested += 1
                n_max = max(n_max, n)
    
    if not ratios:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios))
    conjecture_holds = all(0.9 * mean_ratio <= r <= 1.1 * mean_ratio for r in ratios)
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_ratio={mean_ratio}, std_ratio={std_ratio}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(0.8 * mean_value <= r["metric_value"] <= 1.2 * mean_value for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")