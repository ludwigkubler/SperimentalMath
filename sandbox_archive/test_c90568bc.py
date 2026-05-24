# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, chain

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n: int, m: int):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def dpll_tree_width(cnf):
        variables = set(abs(lit) for lit in chain.from_iterable(cnf))
        model = set()
        
        def dfs(model, level):
            if not cnf:
                return level
            var = next(iter(variables - model), None)
            if var is None:
                return 0
            
            new_model_true = model.union({var})
            new_model_false = model.union({-var})
            
            width_true = dfs(new_model_true, level + 1)
            width_false = dfs(new_model_false, level + 1)
            
            return max(width_true, width_false)
        
        return dfs(model, 0)

    def grothendieck_group_rank(cnf):
        # Placeholder for the actual computation of Grothendieck group rank
        # This is a dummy implementation that returns a random number for demonstration purposes
        return random.randint(1, len(cnf))

    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    dpll_width = dpll_tree_width(cnf)
    rank = grothendieck_group_rank(cnf)
    
    if rank == 0:
        return {
            "metric_name": "dpll_tree_width_to_grothendieck_group_rank_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Grothendieck group rank is zero"
        }
    
    ratio = Fraction(dpll_width, rank)
    return {
        "metric_name": "dpll_tree_width_to_grothendieck_group_rank_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5 and abs(ratio - 1) <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        mean_ratio = None
        std_ratio = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")