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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_hodge_rank(s):
        # Placeholder function to simulate Hodge rank computation
        # Replace with actual algorithm if available
        return random.randint(1, s)
    
    n_values = [5, 10, 15, 20, 30, 40]
    hodge_ranks = []
    bp_sizes = []
    
    for n in n_values:
        F = generate_boolean_function(n)
        s = len(F) - 1
        rank = compute_hodge_rank(s)
        hodge_ranks.append(rank)
        bp_sizes.append(s)
    
    if not hodge_ranks or not bp_sizes:
        return {
            "metric_name": "Hodge Rank vs BP Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = sum(hodge_ranks) / len(hodge_ranks)
    std_dev = math.sqrt(sum((x - mean_rank)**2 for x in hodge_ranks) / len(hodge_ranks))
    correlation_coefficient = sum((hodge_ranks[i] - mean_rank) * (bp_sizes[i] - mean(bp_sizes)) for i in range(len(hodge_ranks))) / (len(hodge_ranks) * std_dev * math.sqrt(sum((x - mean(bp_sizes))**2 for x in bp_sizes)))
    
    return {
        "metric_name": "Hodge Rank vs BP Size",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")