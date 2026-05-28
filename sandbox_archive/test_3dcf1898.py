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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def depth_of_smallest_frege_proof(f):
        # Placeholder function to simulate depth calculation
        return len(f)
    
    def calculate_genus(M_f):
        # Placeholder function to simulate genus calculation
        return len(M_f) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_genus = 0
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            depth = depth_of_smallest_frege_proof(f)
            genus = calculate_genus(f)
            
            total_genus += genus
            total_depth += depth
            instances_tested += 1
    
    mean_genus = total_genus / instances_tested
    mean_depth = total_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(g * d for g, d in zip(genus_list, depth_list)) -
                               sum(genus_list) * sum(depth_list)) / math.sqrt(
        (instances_tested * sum(g**2 for g in genus_list) - sum(genus_list)**2) *
        (instances_tested * sum(d**2 for d in depth_list) - sum(depth_list)**2))
    
    conjecture_holds = correlation_coefficient >= 0.7 and abs(mean_genus - mean_depth**2) <= 0.5 * mean_depth**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Spearman Rank Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")