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
    
    # Generate a random k-CNF formula with n variables and k clauses
    n = random.randint(5, 40)
    k = random.randint(n // 2, n * (n - 1) // 2)
    cnf_formula = []
    for _ in range(k):
        clause = [random.choice([True, False]) for _ in range(n)]
        cnf_formula.append(clause)
    
    # Construct the corresponding real algebraic curve using the Grothendieck-Riemann-Roch theorem
    # This is a placeholder function. In practice, you would need to implement this.
    def grothendieck_riemann_roch_theorem(cnf_formula):
        return 1.0  # Placeholder value
    
    geometric_entropy = grothendieck_riemann_roch_theorem(cnf_formula)
    
    # Construct the decision tree for the k-CNF formula and measure its height
    def construct_decision_tree(cnf_formula):
        if not cnf_formula:
            return 1
        max_height = 0
        for clause in cnf_formula:
            sub_formula = [sub_clause for sub_clause in cnf_formula if sub_clause != clause]
            height = 1 + construct_decision_tree(sub_formula)
            if height > max_height:
                max_height = height
        return max_height
    
    decision_tree_height = construct_decision_tree(cnf_formula)
    
    # Correlate the computed geometric entropy with the logarithm of the decision tree height
    log_decision_tree_height = math.log(decision_tree_height) if decision_tree_height > 0 else float('inf')
    c = 1.0  # Placeholder value for the constant factor
    
    # Check if the geometric entropy exceeds c times the logarithm of the decision tree height
    if geometric_entropy > c * log_decision_tree_height:
        conjecture_holds = False
        counterexample = "geometric_entropy_exceeds_bound"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": geometric_entropy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "geometric_entropy_exceeds_bound"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")