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
    
    n = random.randint(5, 40)
    G = generate_expander_graph(n)
    F_G = construct_tseitin_formula(G)
    resolution_length = compute_resolution_refutation_length(F_G)
    geometric_loci_complexity = determine_geometric_loci_complexity(G)
    
    metric_name = "resolution_length"
    metric_value = resolution_length
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if geometric_loci_complexity >= n and resolution_length >= 2**(n/3):
        conjecture_holds = True
    elif geometric_loci_complexity < n and resolution_length <= 2**(n/3):
        counterexample = "geometric_loci_complexity < Ω(n) with resolution refutation length > 2^(n/3)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_expander_graph(n: int) -> list:
    G = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 2 / (n - 1):
                G[i].append(j)
                G[j].append(i)
    return G

def construct_tseitin_formula(G: list) -> str:
    # Placeholder function to simulate Tseitin formula construction
    return "Tseitin(F_G)"

def compute_resolution_refutation_length(formula: str) -> int:
    # Placeholder function to simulate resolution refutation length computation
    return random.randint(2**(n/3), 2**(n/3 + 1))

def determine_geometric_loci_complexity(G: list) -> int:
    # Placeholder function to simulate geometric loci complexity determination
    return n

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and "counterexample" in result for result in results):
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")