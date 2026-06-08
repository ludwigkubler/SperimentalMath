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
    
    def generate_monomial_representation(n):
        # Generate a random Boolean function with n variables
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_projective_variety(monomial):
        # Simplified computation of projective variety (placeholder)
        return sum(monomial) % 2
    
    def compute_tseitin_formula(monomial):
        # Placeholder function to derive Tseitin formula
        return monomial
    
    def compute_resolution_proof_width(formula):
        # Placeholder function to compute resolution proof width
        return len(formula)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        monomial = generate_monomial_representation(n)
        h = compute_projective_variety(monomial)
        phi = compute_tseitin_formula(monomial)
        w_phi = compute_resolution_proof_width(phi)
        
        if h == 0 or w_phi == 0:
            continue
        
        metric_values.append((h, w_phi))
    
    if not metric_values:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid pairs (h, w) found"
        }
    
    h_values = [h for h, _ in metric_values]
    w_phi_values = [w_phi for _, w_phi in metric_values]
    
    mean_h = sum(h_values) / len(h_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    covariance = sum((h - mean_h) * (w_phi - mean_w_phi) for h, w_phi in metric_values) / len(metric_values)
    variance_h = sum((h - mean_h)**2 for h in h_values) / len(h_values)
    variance_w_phi = sum((w_phi - mean_w_phi)**2 for w_phi in w_phi_values) / len(w_phi_values)
    
    pearson_corr_coeff = covariance / (math.sqrt(variance_h) * math.sqrt(variance_w_phi))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr_coeff >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")