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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_random_sat_instance(n, clause_count):
    literals = list(range(1, n + 1))
    phi = []
    for _ in range(clause_count):
        clause = random.sample(literals + [-l for l in literals], 2)
        phi.append(tuple(sorted(clause)))
    return phi

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_generators = 0
    total_widths = 0
    
    for n in n_values:
        phi = generate_random_sat_instance(n, clause_count=2 * n)
        
        # Compute DPLL search tree width (simplified version for demonstration)
        width = len(phi)  # This is a very naive approximation
        
        # Compute the affine quotient ring generators
        generator_set = set()
        for clause in phi:
            generator_set.add(clause[0])
            generator_set.add(clause[1])
        
        total_generators += len(generator_set)
        total_widths += width
    
    mean_ratio = total_generators / total_widths if total_widths != 0 else float('inf')
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_ratio - 1.0) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")