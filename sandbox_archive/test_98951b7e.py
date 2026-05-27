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
    
    def generate_sat_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def tropical_rank(sat_formula):
        # Placeholder implementation of tropical rank computation
        # This is a dummy function and should be replaced with actual logic
        return len(sat_formula)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per n
            sat_formula = generate_sat_formula(n)
            rank = tropical_rank(sat_formula)
            ranks.append((n, rank))
    
    if not ranks:
        return {
            "metric_name": "tropical_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values = [x for x, _ in ranks]
    ranks = [y for _, y in ranks]
    
    mean_n = sum(n_values) / len(n_values)
    std_n = math.sqrt(sum((x - mean_n)**2 for x in n_values) / len(n_values))
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((y - mean_rank)**2 for y in ranks) / len(ranks))
    
    support_fraction = sum(1 for r in ranks if 0.7 * mean_rank <= r <= 1.3 * mean_rank) / len(ranks)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")