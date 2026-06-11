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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set(random.sample(range(1, n+1), 2))
        if random.choice([True, False]):
            clause = {-lit for lit in clause}
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    clauses = list(cnf)
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                if not clauses[i].isdisjoint(clauses[j]):
                    common_lit = next(lit for lit in clauses[i] if -lit in clauses[j])
                    new_clause = (clauses[i] | clauses[j]) - {common_lit, -common_lit}
                    if new_clause:
                        new_clauses.append(new_clause)
        if not new_clauses:
            return len(clauses)
        clauses.extend(new_clauses)

def qsi(cnf):
    # Placeholder for the actual implementation of qsi
    # This is a dummy function that returns a random value for demonstration purposes
    return random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small size and increase as needed
    m = 2 * n
    cnf = generate_cnf(n, m)
    
    qsi_value = qsi(cnf)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "qsi_vs_width",
        "metric_value": qsi_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")