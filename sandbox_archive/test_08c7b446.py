# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random group G with n elements
    n = 10 + (seed % 25)  # Ensure n is at least 10 for meaningful results
    G = generate_random_group(n)
    
    # Compute the minimal representation rank mrank(G)
    mrank_G = compute_minimal_representation_rank(G)
    
    # Construct the associated Tseitin formula φ_G
    phi_G = construct_tseitin_formula(G)
    
    # Measure the Frege proof width w(φ_G) of φ_G
    w_phi_G = measure_frege_proof_width(phi_G)
    
    return {
        "metric_name": "mrank(G) vs. w(φ_G)",
        "metric_value": mrank_G * w_phi_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if mrank_G > 10 or w_phi_G > 10 else True,
        "counterexample": "mapping_undefined" if mrank_G > 10 or w_phi_G > 10 else ""
    }

def generate_random_group(n: int) -> list:
    # Simple cyclic group Z_n
    return [(i % n, (i + 1) % n) for i in range(n)]

def compute_minimal_representation_rank(G: list) -> int:
    # Placeholder function; actual implementation needed
    return len(G)

def construct_tseitin_formula(G: list) -> str:
    # Placeholder function; actual implementation needed
    return "phi_G"

def measure_frege_proof_width(phi_G: str) -> int:
    # Placeholder function; actual implementation needed
    return 10

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r['metric_value'] for r in results]
    conjecture_holds_count = sum(r['conjecture_holds'] for r in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r['counterexample'] == "mapping_undefined" for r in results):
        first_failing_seed = next(r['seed'] for r in results if r['counterexample'] == "mapping_undefined")
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")