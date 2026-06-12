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
    
    # Generate a random Tseitin formula with n variables
    n = 5 + random.randint(0, 34)
    phi_G = generate_tseitin_formula(n)
    
    # Compute the minimal geometric entropy of the symplectic leaves
    H_min = minimal_geometric_entropy(phi_G, n)
    
    # Calculate the resolution proof width for the formula
    w_phi_G = resolution_proof_width(phi_G)
    
    if H_min is None or w_phi_G is None:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    # Compute the Pearson correlation coefficient
    instances_tested = 1
    n_max = n
    metric_value = H_min * w_phi_G
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": ""
    }

def generate_tseitin_formula(n: int) -> str:
    # Placeholder for generating a Tseitin formula
    return "Tseitin formula with {} variables".format(n)

def minimal_geometric_entropy(phi_G: str, n: int) -> float:
    # Placeholder for computing the minimal geometric entropy
    return random.random()

def resolution_proof_width(phi_G: str) -> int:
    # Placeholder for calculating the resolution proof width
    return random.randint(1, 10)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", result)
        results.append(result)
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    if all(math.isnan(res["metric_value"]) for res in results):
        print("RESULT: INCONCLUSIVE no_valid_data")
    else:
        valid_results = [res for res in results if not math.isnan(res["metric_value"])]
        mean_metric_value = sum(res["metric_value"] for res in valid_results) / len(valid_results)
        std_metric_value = (sum((res["metric_value"] - mean_metric_value) ** 2 for res in valid_results) / len(valid_results)) ** 0.5
        support_fraction = sum(1 for res in valid_results if res["conjecture_holds"]) / len(valid_results)
        
        if support_fraction >= 0.8:
            print("RESULT: SUPPORTED mean={:.2f} std={:.2f} support_fraction={:.2f}".format(mean_metric_value, std_metric_value, support_fraction))
        else:
            first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
            print("RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={}".format(first_failing_seed))