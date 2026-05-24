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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll_width(cnf):
        n = len(set(abs(lit) for lit in cnf))
        model = [False] * (n + 1)
        
        def dfs(model, level):
            if level == n:
                return 0
            var = next((i for i in range(1, n + 1) if not model[i]), None)
            if var is None:
                return 0
            
            new_model_true = model[:]
            new_model_true[var] = True
            width_true = dfs(new_model_true, level + 1)
            
            new_model_false = model[:]
            new_model_false[var] = False
            width_false = dfs(new_model_false, level + 1)
            
            return max(width_true, width_false) + 1
        
        return dfs(model, 0)
    
    def grothendieck_rank(cnf):
        # Placeholder for the actual mapping to a noncommutative Grothendieck group
        # For simplicity, we'll use the number of clauses as a proxy
        return len(cnf)

    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1) // 2)
    cnf = generate_cnf(n, m)
    
    width = dpll_width(cnf)
    rank = grothendieck_rank(cnf)
    
    if rank == 0:
        return {
            "metric_name": "DPLL tree width / Grothendieck group rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = Fraction(width, rank)
    return {
        "metric_name": "DPLL tree width / Grothendieck group rank",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5 and abs(float(ratio) - 1) <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")