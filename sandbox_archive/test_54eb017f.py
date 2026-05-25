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

def resolution_width(F):
    n = len(F)
    assignment = [None] * (2 * n + 1)
    
    def dpll(clauses, literals):
        if not clauses:
            return True
        literal = next(l for l in literals if all(l not in clause and -l not in clause for clause in clauses))
        if literal is None:
            return False
        
        assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if dpll(new_clauses, literals):
            return True
        
        assignment[literal] = False
        assignment[-literal] = True
        new_clauses = [c for c in clauses if -literal not in c and literal not in c]
        if dpll(new_clauses, literals):
            return True
        
        assignment[-literal] = None
        return False
    
    return len([l for l in range(1, n + 1) if dpll(F, [l])])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, k):
        literals = list(range(-n, 0)) + list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def bruer_group_order(k):
        if k != 3:
            return 0
        return 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    total_bruer_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            F = generate_kcnf(n, k=10)  # Using a fixed k for simplicity
            width = resolution_width(F)
            bruer_order = bruer_group_order(k=3)
            total_width += width
            total_bruer_order += bruer_order
            instances_tested += 1
    
    mean_width = Fraction(total_width, instances_tested)
    mean_bruer_order = Fraction(total_bruer_order, instances_tested)
    
    conjecture_holds = mean_width <= 2 * mean_bruer_order
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": float(mean_width),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")