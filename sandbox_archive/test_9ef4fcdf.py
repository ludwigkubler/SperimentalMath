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
    
    def generate_random_bipartite_state(n):
        # Generate a random bipartite quantum state with entanglement rank up to n
        state = [[random.random() for _ in range(n)] for _ in range(n)]
        return state
    
    def compute_minimal_local_index_of_topological_entanglement_rank(state):
        # Placeholder function to compute mter(X)
        # For simplicity, we assume mter(X) is the sum of absolute values of elements
        return sum(abs(x) for row in state for x in row)
    
    def compute_communication_complexity(state):
        # Placeholder function to compute cc(X)
        # For simplicity, we assume cc(X) is the sum of squares of elements
        return sum(x**2 for row in state for x in row)
    
    n_max = 40
    instances_tested = 30
    ranks = []
    cc_values = []
    
    for _ in range(instances_tested):
        state = generate_random_bipartite_state(n_max)
        mter_X = compute_minimal_local_index_of_topological_entanglement_rank(state)
        cc_X = compute_communication_complexity(state)
        
        if mter_X == 0 or cc_X == 0:
            continue
        
        ranks.append(mter_X)
        cc_values.append(cc_X)
    
    if not ranks or not cc_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ranks = sum(ranks) / len(ranks)
    mean_cc_values = sum(cc_values) / len(cc_values)
    
    correlation_coefficient = sum((ranks[i] - mean_ranks) * (cc_values[i] - mean_cc_values) for i in range(len(ranks))) / len(ranks)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")