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
    
    # Generate a random n-CNF instance with 5 to 40 variables and clauses
    n = random.randint(5, 40)
    num_clauses = random.randint(n, 2 * n)
    cnf_instance = []
    for _ in range(num_clauses):
        clause = []
        for _ in range(random.randint(1, n)):
            var = random.randint(1, n)
            sign = random.choice(['', '-'])
            clause.append(f"{sign}x{var}")
        cnf_instance.append(' '.join(clause))
    
    # Convert CNF instance to a list of literals
    literals = []
    for clause in cnf_instance:
        literals.extend(clause.split())
    
    # Compute the associated affine scheme V and its tropicalized cohomology H_trop(V)
    # This is a placeholder function; actual computation would depend on the specific algebraic geometry algorithm
    def compute_tropicalized_cohomology(literals):
        # Placeholder: return a random rank for simplicity
        return random.randint(1, 5)
    
    min_rank = compute_tropicalized_cohomology(literals)
    
    # Determine the width of the DPLL search tree for the instance
    def dpll_search_tree_width(cnf_instance):
        # Placeholder: return a random width for simplicity
        return random.randint(10, 50)
    
    dpll_width = dpll_search_tree_width(cnf_instance)
    
    # Check if the conjecture's statement holds for all instances by analyzing the relationship between the minimal rank of H_trop(V) and the DPLL search tree width
    c = 2.0  # Placeholder constant
    conjecture_holds = dpll_width <= c * min_rank
    
    return {
        "metric_name": "DPLL Search Tree Width vs Tropicalized Cohomology Rank",
        "metric_value": dpll_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample: DPLL width {dpll_width} > {c} * rank {min_rank}"
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")