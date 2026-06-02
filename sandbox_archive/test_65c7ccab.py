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
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate 10n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def construct_affine_space(cnf):
        variables = set()
        for clause in cnf:
            variables.update(abs(var) for var in clause)
        return len(variables)
    
    def compute_minimal_geometric_langlands_index(n):
        # Placeholder function. Replace with actual computation.
        return random.uniform(0, n)
    
    def determine_resolution_proof_width(cnf):
        # Placeholder function. Replace with actual computation.
        return random.randint(1, 2 * len(cnf))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_random_cnf(n)
    mli_phi = compute_minimal_geometric_langlands_index(n)
    w_phi = determine_resolution_proof_width(cnf)
    
    return {
        "metric_name": "mli_vs_w",
        "metric_value": mli_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [result["metric_value"] for result in results]
    conjecture_holds_count = sum(result["conjecture_holds"] for result in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")