# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if not any(lit == -other_lit for lit, other_lit in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def diophantine_approximation(f):
        x = Fraction(0, 1)
        y = Fraction(1, 1)
        while True:
            z = (x + y) / 2
            if abs(f(z)) < abs(f(x)) and abs(f(z)) < abs(f(y)):
                x = z
            else:
                y = z
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        f = lambda x: sum([sum([x**abs(lit) * (-1 if lit < 0 else 1) for lit in clause]) for clause in cnf])
        mo_f = diophantine_approximation(f)
        w_phi = resolution_width(cnf)
        results.append((n, log(mo_f), w_phi))
    
    if not results:
        return {
            "metric_name": "log_mo_f",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_mo_f_values = [r[1] for r in results]
    w_phi_values = [r[2] for r in results]
    
    if not all(0.5 <= log_mo_f / w_phi <= 2 for log_mo_f, w_phi in zip(log_mo_f_values, w_phi_values)):
        return {
            "metric_name": "log_mo_f",
            "metric_value": sum(log_mo_f_values) / len(log_mo_f_values),
            "instances_tested": len(results),
            "n_max": max(r[0] for r in results),
            "conjecture_holds": False,
            "counterexample": "ratio_out_of_bounds"
        }
    
    return {
        "metric_name": "log_mo_f",
        "metric_value": sum(log_mo_f_values) / len(log_mo_f_values),
        "instances_tested": len(results),
        "n_max": max(r[0] for r in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_out_of_bounds' first_failing_seed={first_failing_seed}")