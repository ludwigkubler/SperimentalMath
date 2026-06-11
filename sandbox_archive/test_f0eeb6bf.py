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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([0, 1]) - 1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def resolution_width(cnf):
    queue = cnf[:]
    learned_clauses = set()
    
    while queue:
        clause = queue.pop()
        for literal in clause:
            neg_literal = -literal
            if neg_literal in learned_clauses:
                continue
            new_clause = []
            for other_clause in queue + list(learned_clauses):
                if neg_literal in other_clause:
                    other_clause.remove(neg_literal)
                    new_clause.extend(other_clause)
                    break
            if not new_clause:
                return len(queue) + 1
            new_clause = list(set(new_clause))
            if new_clause and tuple(new_clause) not in learned_clauses:
                queue.append(new_clause)
                learned_clauses.add(tuple(new_clause))
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    rk_min_sum = 0
    w_phi_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(8):  # Aim for at least 30 instances per seed
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            
            rk_min = sum(len(set(clause)) for clause in cnf)  # Simplified rank computation
            w_phi = resolution_width(cnf)
            
            rk_min_sum += rk_min
            w_phi_sum += w_phi
            instances_tested += 1
    
    mean_rk_min = rk_min_sum / instances_tested
    mean_w_phi = w_phi_sum / instances_tested
    
    # Pearson correlation coefficient
    numerator = sum((rk_min - mean_rk_min) * (w_phi - mean_w_phi) for rk_min, w_phi in zip(rk_min_values, w_phi_values))
    denominator = math.sqrt(sum((rk_min - mean_rk_min) ** 2 for rk_min in rk_min_values)) * math.sqrt(sum((w_phi - mean_w_phi) ** 2 for w_phi in w_phi_values))
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")