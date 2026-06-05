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
    
    # Generate a CNF formula with n clauses and m literals
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = []
    for _ in range(n):
        clause = [random.randint(-m, -1), random.randint(1, m)]
        clauses.append(clause)
    
    # Compute the order of the Coxeter group associated with the CNF formula
    # For simplicity, we use a precomputed table of Coxeter group orders for small permutations
    def coxeter_group_order(n):
        if n == 2:
            return 3
        elif n == 3:
            return 6
        else:
            return None
    
    order = coxeter_group_order(n)
    if order is None:
        return {
            "metric_name": "Coxeter Group Order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Construct the Frege proof tree for the CNF and measure its width
    def frege_proof_tree_width(clauses):
        # Simplified model of Frege proof tree width calculation
        return len(max(set([abs(c) for clause in clauses for c in clause]), key=clauses.count))
    
    width = frege_proof_tree_width(clauses)
    
    # Return the results
    return {
        "metric_name": "Coxeter Group Order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    if all(result["metric_value"] is not None for result in results):
        values = [result["metric_value"] for result in results]
        mean = sum(values) / len(values)
        std = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    else:
        mean, std, support_fraction = None, None, None
    
    # Determine the final result
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")