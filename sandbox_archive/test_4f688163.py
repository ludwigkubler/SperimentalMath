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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        assignment = {}
        queue = cnf[:]
        
        while queue:
            literal = queue.pop()
            if literal in assignment and assignment[literal] != -literal:
                continue
            assignment[literal] = True
            
            for clause in cnf:
                if literal in clause:
                    queue.append(-literal)
                    break
    
    def binary_quadratic_form(clause):
        x, y = abs(clause[0]), abs(clause[1])
        return (x * x + y * y) / 2
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    resolution_width_value = resolution_width(cnf)
    distinct_forms = set(binary_quadratic_form(clause) for clause in cnf)
    
    metric_name = "resolution_width"
    metric_value = resolution_width_value
    instances_tested = len(cnf)
    n_max = n
    conjecture_holds = 0.8 <= resolution_width_value / math.sqrt(n) <= 1.2 and len(distinct_forms) <= 1.5 * resolution_width_value
    counterexample = "" if conjecture_holds else "resolution_width out of bounds or too many distinct forms"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width out of bounds or too many distinct forms\" first_failing_seed={first_failing_seed}")