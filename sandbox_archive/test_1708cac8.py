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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def boolean_function(cnf, n):
        assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
        return any(all(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in cnf)
    
    def diophantine_approximation(f, n):
        x = 1.5
        f_n = f(n)
        approx = round(x * f_n)
        return abs(approx - f_n) / f_n
    
    def resolution_width(cnf):
        width = 0
        for clause in cnf:
            if len(clause) > width:
                width = len(clause)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f_n = boolean_function(generate_cnf(n), n)
        mo_f = diophantine_approximation(f_n, n)
        w_n = resolution_width(generate_cnf(n))
        
        if mo_f == 0 or w_n == 0:
            continue
        
        ratio = math.log(mo_f) / w_n
        results.append((ratio, f_n, w_n))
    
    if not results:
        return {
            "metric_name": "log_mo_over_w",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_pairs"
        }
    
    ratios = [r for r, _, _ in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio)**2 for r in ratios) / len(ratios))
    
    conjecture_holds = all(0.5 <= r <= 2 for r, _, _ in results)
    counterexample = "" if conjecture_holds else "out_of_bounds"
    
    return {
        "metric_name": "log_mo_over_w",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")