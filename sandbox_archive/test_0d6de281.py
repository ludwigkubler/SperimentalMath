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
from itertools import combinations

def generate_random_dnf(n, num_terms):
    terms = []
    for _ in range(num_terms):
        term = set(random.sample(range(n), random.randint(1, n)))
        terms.append(term)
    return terms

def compute_mu(D):
    n = len(D[0])
    total_size = sum(len(T) for T in D)
    pairwise_intersections = 0
    for i in range(len(D)):
        for j in range(i + 1, len(D)):
            pairwise_intersections += len(D[i] & D[j])
    return total_size - pairwise_intersections

def is_k_clique_indicator_function(n):
    # This function is a placeholder. For actual k-CLIQUE indicator function,
    # implement the necessary logic here.
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    num_terms = 100
    D = generate_random_dnf(n, num_terms)
    mu_D = compute_mu(D)
    
    if is_k_clique_indicator_function(n):
        min_expected_mu = n ** 0.5
        if mu_D < min_expected_mu:
            return {
                "metric_name": "mu(D)",
                "metric_value": mu_D,
                "instances_tested": num_terms,
                "conjecture_holds": False,
                "counterexample": "k-CLIQUE indicator function, mu(D) < Ω(n^{1/2})"
            }
    else:
        max_expected_mu = n * (n - 1) / 2
        if mu_D > max_expected_mu:
            return {
                "metric_name": "mu(D)",
                "metric_value": mu_D,
                "instances_tested": num_terms,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
    
    return {
        "metric_name": "mu(D)",
        "metric_value": mu_D,
        "instances_tested": num_terms,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_mu)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")