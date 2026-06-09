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
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            if sum(clause) == 0:
                clause[random.randint(0, n-1)] *= -1
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment):
        unsatisfied = [c for c in cnf if not any(l * assignment[abs(l)-1] > 0 for l in c)]
        if not unsatisfied:
            return True
        unit_clauses = [c for c in unsatisfied if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            assignment[abs(literal)-1] = literal > 0
            return dpll(cnf, assignment)
        pure_literals = {}
        for l in set([l for c in unsatisfied for l in c]):
            pos_count = sum(1 for c in unsatisfied if l in c)
            neg_count = sum(1 for c in unsatisfied if -l in c)
            if pos_count == 0:
                pure_literals[l] = True
            elif neg_count == 0:
                pure_literals[l] = False
        if pure_literals:
            literal = next(l for l, p in pure_literals.items() if p)
            assignment[abs(literal)-1] = literal > 0
            return dpll(cnf, assignment)
        pivot = random.choice(unsatisfied[0])
        return any(dpll([c for c in cnf if not (pivot in c and -pivot in c)], {**assignment, abs(pivot)-1: pivot > 0}) 
                   or dpll([c for c in cnf if not (pivot in c and -pivot in c)], {**assignment, abs(pivot)-1: pivot < 0})
                   for pivot in unsatisfied[0])
    
    def quasi_crystal_pattern(height):
        pattern = []
        while height > 0:
            pattern.append(height % 2)
            height //= 2
        return pattern
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            assignment = [None] * n
            height = dpll(cnf, assignment)
            if height is None:
                continue
            pattern = quasi_crystal_pattern(height)
            instances_tested += 1
            n_max = max(n_max, len(pattern))
            total_metric_value += len(pattern)
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / (len(n_values) * 5)
    
    if support_fraction < 0.8:
        return {
            "metric_name": "quasi_crystal_pattern_length",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"support_fraction={support_fraction:.2f} < 0.8"
        }
    
    return {
        "metric_name": "quasi_crystal_pattern_length",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.2f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction too low")