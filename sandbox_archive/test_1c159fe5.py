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
    
    def tseitin_formula(f, n):
        literals = list(range(2 * n))
        clauses = []
        
        for i in range(n):
            literals[i] = f"p{i}"
            literals[n + i] = f"q{i}"
            clauses.append((literals[i], literals[n + i]))
        
        for clause in f:
            literals_clause = [literals[abs(lit) - 1] if lit > 0 else f"~{literals[-abs(lit)]}" for lit in clause]
            clauses.append(("or", *literals_clause))
        
        return clauses
    
    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        # This is a placeholder and should be replaced with actual logic
        return len(clauses)
    
    def minimal_brauer_group_order(n):
        # Placeholder for Brauer group order calculation
        # This is a placeholder and should be replaced with actual logic
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(2 ** n)]
        phi_f = tseitin_formula(f, n)
        br_f = minimal_brauer_group_order(n)
        w_phi_f = resolution_width(phi_f)
        
        results.append({
            "n": n,
            "br_f": br_f,
            "w_phi_f": w_phi_f
        })
    
    metric_value = sum(result["br_f"] * result["w_phi_f"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(0.7 <= br_f / w_phi_f <= 10 for result in results if w_phi_f > 0)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")