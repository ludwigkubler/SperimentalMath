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
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_clause_tree_width(clauses):
        # Simplified heuristic to estimate clause tree width
        return len(clauses) ** 0.5
    
    def quotient_group_size(n):
        # Simplified heuristic for the size of the quotient group
        return n * (n - 1)
    
    def ternary_representations_count(size):
        # Simplified heuristic for the number of ternary representations
        return math.ceil(math.log2(size))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    clause_tree_width = compute_clause_tree_width(cnf)
    group_size = quotient_group_size(n)
    ternary_count = ternary_representations_count(group_size)
    
    if not (n**2 * math.log(n) <= clause_tree_width <= n**2 * math.log(n)):
        return {
            "metric_name": "clause_tree_width",
            "metric_value": clause_tree_width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Clause tree width {clause_tree_width} not in Ω(n^2 log n)"
        }
    
    if ternary_count > n**3 * math.log(n)**3:
        return {
            "metric_name": "ternary_representations",
            "metric_value": ternary_count,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Ternary representations {ternary_count} not polynomially related to n"
        }
    
    return {
        "metric_name": "clause_tree_width",
        "metric_value": clause_tree_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")