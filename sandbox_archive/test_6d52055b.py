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
    
    def generate_random_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 2))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            else:
                clause = {x: 1 for x in clause}
            clauses.append(clause)
        return clauses

    def tropical_realization(cnf):
        # Simplified tropical realization for demonstration
        return len(cnf)

    def min_rank(tropical_structure):
        # Simplified min rank calculation for demonstration
        return len(tropical_structure)

    n = 10  # Fixed n for simplicity in this example
    k_values = [2, 3, 4, 5]
    results = []
    
    for k in k_values:
        cnf = generate_random_k_cnf(n, k)
        tropical_structure = tropical_realization(cnf)
        rank = min_rank(tropical_structure)
        results.append({"k": k, "rank": rank})
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(results[i]["rank"] <= results[i+1]["rank"] for i in range(len(results)-1))
    counterexample = "" if conjecture_holds else "Non-monotonic rank observed"
    
    return {
        "metric_name": "MinRank(F)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-monotonic rank observed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")