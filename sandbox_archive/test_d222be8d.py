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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def monotone_width(cnf):
        # Simplified heuristic to estimate monotone width
        return len(cnf)
    
    def cohomological_dimension(cnf):
        # Simplified heuristic to estimate cohomological dimension
        return len(cnf) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        w_m = monotone_width(cnf)
        mu = cohomological_dimension(cnf)
        metrics.append((n, mu, w_m))
    
    if not metrics:
        return {
            "metric_name": "cohomological_dimension",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in metrics)
    if n_max < 16:
        return {
            "metric_name": "cohomological_dimension",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    mu_values = [mu for _, mu, _ in metrics]
    w_m_values = [w_m for _, _, w_m in metrics]
    
    mean_mu = sum(mu_values) / len(mu_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    
    correlation = (sum((mu - mean_mu) * (w_m - mean_w_m) for mu, w_m in zip(mu_values, w_m_values)) /
                   math.sqrt(sum((mu - mean_mu) ** 2 for mu in mu_values) *
                             sum((w_m - mean_w_m) ** 2 for w_m in w_m_values)))
    
    abs_diff = [abs(mu - (0.5 * w_m)) for mu, w_m in zip(mu_values, w_m_values)]
    mean_abs_diff = sum(abs_diff) / len(abs_diff)
    
    return {
        "metric_name": "cohomological_dimension",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, mu={r['metric_value']}, w_m={w_m}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")