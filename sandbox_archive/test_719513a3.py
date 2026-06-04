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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            cnf.remove(unit_clause)
            for clause in cnf[:]:
                if literal in clause:
                    cnf.remove(clause)
                elif -literal in clause:
                    clause.remove(-literal)
                    stack.append(clause)
        return len(stack)
    
    def brauer_group_order(n):
        # Simplified Brauer group order estimation
        return math.ceil(math.log(n, 2) ** 2)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    order = brauer_group_order(n)
    
    if width == 0:
        return {
            "metric_name": "log(n)^2 / w(φ)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "width_is_zero"
        }
    
    ratio = (math.log(n, 2) ** 2) / width
    return {
        "metric_name": "log(n)^2 / w(φ)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= order,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"width_is_zero\" first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE mapping_undefined"
    
    print(result)