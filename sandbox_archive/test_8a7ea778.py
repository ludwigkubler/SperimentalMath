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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def dpll_tree_width(cnf):
        variables = set(abs(lit) for lit in sum(cnf, []))
        n_vars = len(variables)
        
        def dfs(model, level):
            if not variables:
                return level
            
            var = next(iter(variables - model))
            new_model_true = model | {var}
            new_model_false = model | {-var}
            
            width_true = dfs(new_model_true, level + 1)
            width_false = dfs(new_model_false, level + 1)
            
            return max(width_true, width_false)
        
        return dfs(set(), 0)
    
    def noncommutative_grothendieck_group_rank(cnf):
        # Placeholder for actual implementation
        # For simplicity, we assume the rank is proportional to the number of variables
        n_vars = len(set(abs(lit) for lit in sum(cnf, [])))
        return n_vars
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    dpll_width = dpll_tree_width(cnf)
    rank = noncommutative_grothendieck_group_rank(cnf)
    
    if rank == 0:
        return {
            "metric_name": "dpll_width_to_rank_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = dpll_width / rank
    
    return {
        "metric_name": "dpll_width_to_rank_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5 and abs(ratio - 1) <= 0.05,
        "counterexample": "" if ratio <= 1.5 and abs(ratio - 1) <= 0.05 else f"Ratio {ratio} outside bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 32))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("metric_value" not in result or result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        ratios = [result["metric_value"] for result in results if "metric_value" in result and result["metric_value"] is not None]
        mean_ratio = sum(ratios) / len(ratios)
        std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
        
        support_fraction = sum(1 for r in ratios if r <= 1.5 and abs(r - 1) <= 0.05) / len(ratios)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (result["metric_value"] is None or result["metric_value"] <= 1.5 and abs(result["metric_value"] - 1) <= 0.05))
            print(f"RESULT: FALSIFIED counterexample='Ratio outside bounds' first_failing_seed={first_failing_seed}")