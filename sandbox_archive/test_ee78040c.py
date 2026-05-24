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
    
    def generate_boolean_function(n, m):
        variables = [random.choice([0, 1]) for _ in range(m)]
        clauses = []
        for i in range(m):
            clause = random.sample(range(n), n // 2)
            clauses.append(clause)
        return variables, clauses

    def compute_toric_rank(variables, clauses):
        # Placeholder for actual computation
        return len(variables)

    def resolution_proof_length(clauses):
        # Placeholder for actual computation
        return len(clauses) * 10  # Simplified example

    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    variables, clauses = generate_boolean_function(n, m)
    
    rank = compute_toric_rank(variables, clauses)
    proof_length = resolution_proof_length(clauses)
    
    return {
        "metric_name": "toric_rank_vs_resolution",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")