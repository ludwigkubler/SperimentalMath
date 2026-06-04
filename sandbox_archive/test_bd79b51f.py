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

# Helper functions for CNF generation and resolution proof width computation
def generate_cnf(n, m):
    cnf = []
    literals = list(range(1, n + 1)) + [-x for x in range(1, n + 1)]
    for _ in range(m):
        clause = random.sample(literals, random.randint(2, n))
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    width = 0
    while True:
        new_clauses = []
        for clause1 in clauses:
            for clause2 in clauses:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
        if not new_clauses:
            break
        clauses.update(new_clauses)
        width += 1
    return width

def hodge_complexity(cnf):
    # Placeholder for Hodge complexity computation
    # This is a stub and should be replaced with actual implementation
    return len(cnf)

# Main function to run one trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
        h = hodge_complexity(cnf)
        w = resolution_width(cnf)
        results.append({"n": n, "h": h, "w": w})
    
    mean_w = sum(result["w"] for result in results) / len(results)
    mean_h2 = sum(result["h"] ** 2 for result in results) / len(results)
    diff = abs(mean_w - mean_h2)
    
    conjecture_holds = diff <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_w,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main execution block
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_w = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_w) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_w} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_w} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")