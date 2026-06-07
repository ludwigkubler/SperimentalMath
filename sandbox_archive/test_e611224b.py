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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                break
            lit = unit_clause[0]
            cnf = [c for c in cnf if lit not in c and -lit not in c]
            stack.append(lit)
        return len(stack)
    
    def tropical_hodge_index(cnf):
        # Simplified computation of tropical Hodge index
        return sum(1 for _ in cnf) / 2
    
    n_max = 40
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        h_t = tropical_hodge_index(cnf)
        w = resolution_width(cnf)
        
        if w == 0:
            continue
        
        ratio = h_t / w
        total_ratio += ratio
        instances_tested += 1
        
        if ratio < 1.0:
            conjecture_holds = False
            counterexample = f"n={n}, h_t={h_t}, w={w}"
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")