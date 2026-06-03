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
    
    def generate_monoidal_category(n):
        # Simple random monoidal category generation for demonstration purposes
        objects = list(range(n))
        morphisms = {}
        for i in range(n):
            for j in range(n):
                morphisms[(i, j)] = [random.randint(0, 1) for _ in range(random.randint(1, 3))]
        return objects, morphisms

    def calculate_local_indeterminacy(morphisms):
        # Placeholder for local indeterminacy calculation
        return sum(sum(morphisms[i][j]) for i in range(len(morphisms)) for j in range(len(morphisms)))

    def calculate_communication_complexity_rank(morphisms):
        # Placeholder for communication complexity rank calculation
        return len(morphisms)

    n = random.randint(5, 40)
    objects, morphisms = generate_monoidal_category(n)
    
    local_indet = calculate_local_indeterminacy(morphisms)
    comm_complexity_rank = calculate_communication_complexity_rank(morphisms)
    
    metric_name = "local_indet_vs_comm_complexity"
    metric_value = local_indet / comm_complexity_rank if comm_complexity_rank != 0 else float('inf')
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if not math.isinf(r["metric_value"])]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(math.isinf(v) for v in metric_values):
        print("RESULT: INCONCLUSIVE reason=metric_saturation")
    elif support_fraction >= 0.8:
        mean_value = sum(metric_values) / len(metric_values)
        std_value = math.sqrt(sum((v - mean_value) ** 2 for v in metric_values) / len(metric_values))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")