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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def truth_table_to_clauses(truth_table):
    n = int(truth_table[0].index('1'))
    clauses = []
    for i in range(2**n):
        clause = []
        for j in range(n):
            if (i >> j) & 1:
                clause.append(f"x{j+1}")
            else:
                clause.append(f"~x{j+1}")
        clauses.append(" | ".join(clause))
    return " & ".join(clauses)

def resolution_proof_width(truth_table):
    n = int(truth_table[0].index('1'))
    clauses = truth_table_to_clauses(truth_table).split(" & ")
    literals_i = set()
    for i in range(len(clauses)):
        literals_i.update(set(clause.split(" | ") for clause in clauses[i].split(" | ")))
    return len(literals_i)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        truth_table = generate_boolean_function(n)
        width = resolution_proof_width(truth_table)
        M = len(truth_table)  # Number of monoid objects is the number of clauses
        
        results.append({
            "n": n,
            "width": width,
            "M": M
        })
    
    metric_value = sum(result["M"] / result["width"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(abs(result["M"] - result["width"]) <= 2 * result["width"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "M/W ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")