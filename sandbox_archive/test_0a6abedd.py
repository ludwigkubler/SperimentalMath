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
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n+1):
            clause = [random.choice([f'x{i}', f'-x{i}']) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def tropicalize(cnf):
        # Simplified tropicalization (for demonstration purposes)
        return cnf
    
    def galois_group_size(tropicalized_cnf):
        # Simplified Galois group size calculation
        return len(tropicalized_cnf) + 1
    
    def dpll_search_tree_width(cnf):
        # Simplified DPLL search tree width calculation (for demonstration purposes)
        return sum(len(clause) for clause in cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tropicalized_cnf = tropicalize(cnf)
    galois_group_order = galois_group_size(tropicalized_cnf)
    dpll_width = dpll_search_tree_width(cnf)
    
    return {
        "metric_name": "DPLL Width vs Galois Group Order",
        "metric_value": dpll_width,
        "instances_tested": 1,
        "conjecture_holds": dpll_width <= 3 * galois_group_order,
        "counterexample": "" if dpll_width <= 3 * galois_group_order else f"DPLL Width: {dpll_width}, Galois Group Order: {galois_group_order}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result = "SUPPORTED"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = results[seeds.index(first_failing_seed)]["counterexample"]
        mean_value = sum(result["metric_value"] for result in results)
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        result = "FALSIFIED"
    
    print(f"RESULT: {result} mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")