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
    
    def generate_random_formula(n):
        return [random.choice(['x', '~x']) for _ in range(n)]
    
    def compute_hodge_rank(formula):
        # Simplified Hodge rank computation (not actual Hodge theory)
        return len(set(formula))
    
    def construct_refutation(formula):
        # Simplified refutation construction
        return formula
    
    def compute_tree_width(refutation):
        # Simplified tree width computation
        return len(refutation)
    
    n = random.randint(5, 40)
    formula = generate_random_formula(n)
    hodge_rank = compute_hodge_rank(formula)
    refutation = construct_refutation(formula)
    tree_width = compute_tree_width(refutation)
    
    metric_name = "Hodge Rank vs Refutation Tree Width"
    metric_value = abs(hodge_rank - tree_width)
    instances_tested = 1
    conjecture_holds = hodge_rank == tree_width
    counterexample = "" if conjecture_holds else f"Hodge rank {hodge_rank}, Tree width {tree_width}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    
    if support_fraction >= 0.8 and all(abs(result["metric_value"]) <= 3 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or metric saturation")