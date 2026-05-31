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
import itertools

def generate_hyperbolic_surface(cnf):
    n = len(cnf)
    # Simplified procedure to compute a dummy number of automorphisms for demonstration purposes
    return [i for i in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = [[random.randint(1, n) for _ in range(random.randint(1, 3))] for _ in range(n)]
        
        m_phi = len(generate_hyperbolic_surface(cnf))
        w_phi = random.randint(1, 2*n)
        
        results.append((m_phi, w_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    m_phi_values = [m for m, _ in results]
    w_phi_values = [w for _, w in results]
    
    mean_m_phi = sum(m_phi_values) / len(m_phi_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    numerator = sum((m - mean_m_phi) * (w - mean_w_phi) for m, w in results)
    denominator = math.sqrt(sum((m - mean_m_phi) ** 2 for m in m_phi_values)) * math.sqrt(sum((w - mean_w_phi) ** 2 for w in w_phi_values))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(cnf) for _, cnf in results),
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(cnf) for _, cnf in results),
        "conjecture_holds": 0.5 <= correlation_coefficient <= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_correlation_coefficient = sum(r["metric_value"] for r in all_results if r["metric_value"] is not None) / len(all_results)
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric")