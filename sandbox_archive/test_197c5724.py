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
        for _ in range(3 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 5))]
            if all(abs(lit) <= n for lit in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        return len(cnf)
    
    def p_adic_differential(p, cnf):
        # Constructive mapping to compute p-adic differential
        diff = [0] * (len(cnf) + 1)
        for clause in cnf:
            for lit in clause:
                if lit % p == 0:
                    diff[lit // p] += 1
        return diff
    
    n = random.randint(5, 30)
    cnf = generate_cnf(n)
    w_phi = resolution_width(cnf)
    
    min_diff = float('inf')
    for p in range(2, 10):
        diff = p_adic_differential(p, cnf)
        min_diff = min(min_diff, min(abs(x) for x in diff))
    
    return {
        "metric_name": "min_p_adic_diff",
        "metric_value": min_diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_diff <= w_phi * 2 and min_diff >= w_phi / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.4f} support_fraction={support_fraction:.4f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")