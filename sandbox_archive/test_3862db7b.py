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
from math import log2

def generate_cnf(n):
    cnf = []
    for _ in range(10):  # Generate 10 clauses
        clause = [random.randint(-n, n) for _ in range(3)]
        if any(abs(x) == n for x in clause):  # Ensure no variable is its negation
            continue
        cnf.append(clause)
    return cnf

def compute_frobenius_schur_indicator(cnf):
    # Placeholder implementation; actual computation depends on the vector space associated with CNF
    return random.random()

def compute_entropy(cnf):
    num_clauses = len(cnf)
    if num_clauses == 0:
        return 0
    p = num_clauses / (2 ** n)  # Simplified probability for demonstration
    entropy = -p * log2(p) - (1 - p) * log2(1 - p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size with 5 instances
            cnf = generate_cnf(n)
            mu_phi = compute_frobenius_schur_indicator(cnf)
            H_phi = compute_entropy(cnf)
            
            results.append({
                "n": n,
                "mu_phi": mu_phi,
                "H_phi": H_phi
            })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mu_values = [r["mu_phi"] for r in results]
    H_values = [r["H_phi"] for r in results]
    
    mean_mu = sum(mu_values) / len(mu_values)
    mean_H = sum(H_values) / len(H_values)
    
    correlation_coefficient = sum((mu - mean_mu) * (H - mean_H) for mu, H in zip(mu_values, H_values)) / (
        len(results) * sum((mu - mean_mu) ** 2 for mu in mu_values) * sum((H - mean_H) ** 2 for H in H_values)
    )
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")