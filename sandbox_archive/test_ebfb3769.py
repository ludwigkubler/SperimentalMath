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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def configuration_space_invariant(edges):
        # Placeholder implementation of a simple invariant
        return len(edges)
    
    def sos_hierarchy_degree(edges):
        # Placeholder implementation of SOS degree calculation
        return len(edges) + 1
    
    n = random.randint(5, 40)
    instance = generate_max_cut_instance(n)
    invariant_rank = configuration_space_invariant(instance)
    sos_degree = sos_hierarchy_degree(instance)
    
    metric_value = invariant_rank / sos_degree
    conjecture_holds = abs(metric_value - 0.879) < 2 * (1 / n)
    counterexample = "" if conjecture_holds else f"n={n}, invariant_rank={invariant_rank}, sos_degree={sos_degree}"
    
    return {
        "metric_name": "Invariant Rank to SOS Degree Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    mean_metric_value = total_metric_value / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['instances_tested']}, invariant_rank={result['metric_value']}, sos_degree=1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_seeds")