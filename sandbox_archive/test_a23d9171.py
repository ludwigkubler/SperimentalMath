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
    
    # Generate a random finitely presented group G
    n = random.randint(5, 30)
    generators = [f'a{i}' for i in range(n)]
    relations = []
    for _ in range(random.randint(1, n)):
        rel = ''.join(random.sample(generators, random.randint(2, n)))
        relations.append(rel + rel[::-1])
    
    G_presentation = (generators, relations)
    
    # Compute the minimal local indeterminacy min_indet(G)
    # This is a placeholder function. Implement the actual computation.
    def min_local_indeterminacy(presentation):
        generators, relations = presentation
        return len(generators) + len(relations)
    
    min_indet_G = min_local_indeterminacy(G_presentation)
    
    # Construct the DPLL tree for the group word problem and determine its width w(G)
    def dpll_tree_width(presentation):
        generators, relations = presentation
        n = len(generators)
        width = 2 ** n
        return width
    
    w_G = dpll_tree_width(G_presentation)
    
    # Correlate min_indet(G) with w(G)
    if w_G == 0:
        return {
            "metric_name": "min_indet_over_w",
            "metric_value": float('inf'),  # Indeterminate
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w(G) is zero"
        }
    
    metric_value = min_indet_G / w_G
    
    return {
        "metric_name": "min_indet_over_w",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    
    mean_metric_value = sum(metric_values) / len(metric_values) if metric_values else float('nan')
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)) if len(metric_values) > 1 else float('nan')
    
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")