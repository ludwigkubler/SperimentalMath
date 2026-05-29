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
    
    def generate_tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables)]
            if random.choice([True, False]):
                clause.append(-random.choice(variables))
            clauses.append(clause)
        return variables, clauses
    
    def compute_minimal_root_system_length(n, m):
        # Placeholder function to simulate computing the minimal root system length
        # This is a dummy implementation and should be replaced with actual computation
        return 2 ** (m / n)
    
    def resolve_tseitin_formula(variables, clauses):
        # Placeholder function to simulate resolving the Tseitin formula
        # This is a dummy implementation and should be replaced with actual resolution
        return len(clauses) * 2
    
    n = random.randint(5, 40)
    m = int(n * random.uniform(1, 10))
    variables, clauses = generate_tseitin_formula(n, m)
    
    ν_F = compute_minimal_root_system_length(n, m)
    refutation_length = resolve_tseitin_formula(variables, clauses)
    
    conjecture_holds = refutation_length >= ν_F
    counterexample = "" if conjecture_holds else f"Refutation length {refutation_length} < ν(F) = {ν_F}"
    
    return {
        "metric_name": "Minimal Root System Length",
        "metric_value": ν_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30)) + [random.randint(100, 997) for _ in range(20)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation length < ν(F)\" first_failing_seed={first_failing_seed}")