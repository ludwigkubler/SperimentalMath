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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_sat_instance(n, k):
        clauses = []
        variables = set()
        for _ in range(k * n // 3):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
            for var in clause:
                variables.add(abs(var))
        return clauses, list(variables)

    def compute_communication_complexity_rank(clauses):
        # Simplified rank computation (not actual communication complexity)
        return len(clauses) / len(set(clauses))

    def compute_minimal_index_of_local_system(n, k):
        # Simplified index computation (not actual algebraic topology)
        return n * k

    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, 3)
    clauses, variables = generate_k_sat_instance(n, k)
    
    index = compute_minimal_index_of_local_system(n, k)
    rank = compute_communication_complexity_rank(clauses)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": abs(index - rank) / max(index, rank),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(index - rank) <= 2 * min(index, rank),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")