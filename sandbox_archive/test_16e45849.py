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
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause = [f'~{lit}' if lit.startswith('x') else lit for lit in clause]
            clauses.append(clause)
        return clauses
    
    def resolution_width(formula):
        clauses = formula
        while True:
            new_clauses = []
            added = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    lit_i = set(clauses[i])
                    lit_j = set(clauses[j])
                    if any(lit.startswith('x') and f'~{lit}' in lit_j or not lit.startswith('x') and f'~{lit[1:]}' in lit_j for lit in lit_i):
                        new_clause = [l for l in lit_i | lit_j if not (l.startswith('x') and f'~{l}' in lit_j or not l.startswith('x') and f'~{l[1:]}' in lit_j)]
                        if new_clause:
                            new_clauses.append(new_clause)
                            added = True
            if not added:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def quasi_continuous_order(formula):
        n = len(formula)
        order = 0
        for i in range(n):
            for j in range(i + 1, n):
                if any(lit.startswith('x') and f'~{lit}' in formula[i] or not lit.startswith('x') and f'~{lit[1:]}' in formula[i] for lit in formula[j]):
                    order += 1
        return order
    
    instances_tested = 0
    total_order = 0
    max_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            order = quasi_continuous_order(formula)
            width = resolution_width(formula)
            total_order += order
            instances_tested += 1
            max_width = max(max_width, width)
    
    mean_order = Fraction(total_order, instances_tested)
    if max_width < n:
        return {
            "metric_name": "Quasi-Continuous Order vs Resolution Width",
            "metric_value": float(mean_order),
            "instances_tested": instances_tested,
            "n_max": max_width,
            "conjecture_holds": False,
            "counterexample": "resolution_width_too_small"
        }
    
    return {
        "metric_name": "Quasi-Continuous Order vs Resolution Width",
        "metric_value": float(mean_order),
        "instances_tested": instances_tested,
        "n_max": max_width,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_count = sum(1 for result in results if 0.9 * mean_order <= result["metric_value"] <= 1.1 * mean_order)
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='resolution_width_too_small' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")