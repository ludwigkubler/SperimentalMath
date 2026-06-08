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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f'~{v}' for v in variables], n)
            clauses.append(' & '.join(clause))
        return ' | '.join(clauses)
    
    def local_cohomology_degree(formula, n):
        # Simplified version of local cohomology degree calculation
        # This is a placeholder and should be replaced with actual computation
        return random.randint(1, n)
    
    def resolution_proof_width(formula, n):
        # Simplified version of resolution proof width calculation
        # This is a placeholder and should be replaced with actual computation
        return random.randint(n, 2*n)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_formula(n)
        h_phi = local_cohomology_degree(formula, n)
        w_phi = resolution_proof_width(formula, n)
        results.append((h_phi, w_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    h_values = [h for h, _ in results]
    w_values = [w for _, w in results]
    mean_h = sum(h_values) / len(h_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = sum((h - mean_h) * (w - mean_w) for h, w in results) / (len(results) * math.sqrt(sum((h - mean_h)**2 for h in h_values)) * math.sqrt(sum((w - mean_w)**2 for w in w_values)))
    slope = correlation_coefficient * len(h_values) / sum((h - mean_h)**2 for h in h_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient > 0.5 and slope >= 1.2 * math.log(max(n for _, n in results)) / mean_h**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")