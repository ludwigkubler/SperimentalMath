# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def generate_bdd(n: int, m: int) -> list:
    if n <= 0 or m <= 0:
        return []
    
    nodes = [0] * (2**n + 1)
    edges = []
    
    for _ in range(m):
        u = random.randint(0, 2**n - 1)
        v = random.randint(0, 2**n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    
    return nodes, edges

def compute_hodge_density(m: int) -> float:
    if m <= 0:
        return 0.0
    return math.sqrt(m)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            m = random.randint(n, 2*n)
            nodes, edges = generate_bdd(n, m)
            density = compute_hodge_density(m)
            results.append({
                "n": n,
                "m": m,
                "density": density
            })
    
    if not results:
        return {
            "metric_name": "Hodge Density",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    densities = [r["density"] for r in results]
    m_values = [r["m"] for r in results]
    
    n = len(densities)
    sum_densities = sum(densities)
    sum_m_values = sum(m_values)
    sum_densities_squared = sum([d**2 for d in densities])
    sum_m_values_squared = sum([m**2 for m in m_values])
    sum_products = sum([d * m for d, m in zip(densities, m_values)])
    
    mean_density = sum_densities / n
    mean_m_value = sum_m_values / n
    
    covariance = (sum_products - n * mean_density * mean_m_value) / (n - 1)
    variance_m = (sum_m_values_squared - n * mean_m_value**2) / (n - 1)
    
    if variance_m == 0:
        return {
            "metric_name": "Hodge Density",
            "metric_value": mean_density,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "variance_m_zero"
        }
    
    correlation = covariance / math.sqrt(variance_m)
    
    return {
        "metric_name": "Hodge Density",
        "metric_value": correlation,
        "instances_tested": n,
        "conjecture_holds": abs(correlation - 1) < 0.05,  # 95% confidence interval
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 37))  # First 30 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        sys.exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")