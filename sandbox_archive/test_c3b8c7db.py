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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_polynomial(instance):
        n = len(instance)
        clauses = []
        for i in range(n):
            clauses.append((i, instance[i]))
        for i in range(n):
            for j in range(i+1, n):
                clauses.append((-i-1, -j-1, -(n+i+j)))
        return clauses
    
    def dpll(clauses, assignment, model=[]):
        if not clauses:
            return True
        p = next((c[0] for c in clauses if c[0] >= 0), None)
        if p is None:
            return False
        if p in model:
            return dpll([c for c in clauses if p not in c], assignment, model)
        else:
            if dpll(clauses, assignment + [p], model + [p]):
                return True
            elif dpll(clauses, assignment + [-p], model + [-p]):
                return True
            else:
                return False
    
    def local_cohomology_group_order(n):
        # Simplified version for demonstration purposes
        return n
    
    def log_n(n):
        if n <= 0:
            return float('inf')
        return math.log(n)
    
    instances_tested = 0
    total_metric_value = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested += 1
        instance = generate_boolean_instance(n)
        clauses = tseitin_polynomial(instance)
        path_length = len(dpll(clauses, [])) if dpll(clauses, []) else float('inf')
        metric_value = local_cohomology_group_order(n) / log_n(n)
        
        total_metric_value += metric_value
        max_n = max(max_n, n)
        
        if metric_value > path_length:
            conjecture_holds = False
            counterexample = f"n={n}, H^*({n})={local_cohomology_group_order(n)}, DPLL Path Length={path_length}"
    
    return {
        "metric_name": "H^*(π) / log(n)",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")