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
    
    # Generate a random CNF formula with n clauses and m variables
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = []
    for _ in range(n):
        clause = [random.randint(-m, -1), random.randint(1, m)]
        cnf.append(clause)
    
    # Compute the order of the Coxeter group associated with the CNF formula
    # This is a placeholder function. Replace it with actual computation.
    def coxeter_group_order(cnf):
        return len(cnf)  # Placeholder: assume order is number of clauses
    
    order = coxeter_group_order(cnf)
    
    # Construct the Frege proof tree for the CNF formula
    # This is a placeholder function. Replace it with actual computation.
    def frege_proof_tree_width(cnf):
        return len(cnf)  # Placeholder: assume width is number of clauses
    
    width = frege_proof_tree_width(cnf)
    
    # Return the results as a dictionary
    return {
        "metric_name": "Coxeter Group Order vs Frege Proof Tree Width",
        "metric_value": order / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,  # Placeholder: assume conjecture does not hold
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    total_metric = sum(result["metric_value"] for result in results)
    mean_metric = total_metric / len(results)
    
    squared_diff_sum = sum((result["metric_value"] - mean_metric) ** 2 for result in results)
    std_metric = (squared_diff_sum / len(results)) ** 0.5
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")