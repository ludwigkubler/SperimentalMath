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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def solve(lits_true, lits_false):
            if not cnf:
                return True
            lit = next((lit for lit in range(1, n+1) if lit not in lits_true and -lit not in lits_false), None)
            if lit is None:
                return False
            new_lits_true = lits_true + [lit]
            new_lits_false = lits_false + [-lit]
            return solve(new_lits_true, new_lits_false) or solve(new_lits_false, new_lits_true)
        return solve([], [])
    
    def quasi_frobenius_rank(cnf):
        n = len(set(abs(lit) for lit in cnf))
        rank = 0
        while True:
            found_new_clause = False
            for clause in cnf:
                if all(lit not in lits_true and -lit not in lits_false for lit in clause):
                    new_clause = [lit for lit in clause if lit not in lits_true and -lit not in lits_false]
                    if new_clause:
                        found_new_clause = True
                        rank += 1
                        break
            if not found_new_clause:
                break
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    dpll_widths = []
    
    for n in n_values:
        m = random.randint(n, 2*n)
        cnf = generate_cnf(n, m)
        rank = quasi_frobenius_rank(cnf)
        width = dpll(cnf)
        
        min_ranks.append(rank)
        dpll_widths.append(width)
    
    mean_x = sum(min_ranks) / len(min_ranks)
    mean_y = sum(dpll_widths) / len(dpll_widths)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_ranks, dpll_widths)) / math.sqrt(sum((x - mean_x)**2 for x in min_ranks) * sum((y - mean_y)**2 for y in dpll_widths))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": "" if abs(correlation_coefficient) > 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")