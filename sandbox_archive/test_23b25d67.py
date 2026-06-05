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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        var = next((v for v in range(1, len(assignment) + 2) if v not in assignment), None)
        if var is None:
            return False
        
        pos_var = var
        neg_var = -var
        pos_clauses = [c for c in cnf if any(x == pos_var for x in c)]
        neg_clauses = [c for c in cnf if any(x == neg_var for x in c)]
        
        if dpll(pos_clauses, assignment | {pos_var: True}):
            return True
        elif dpll(neg_clauses, assignment | {neg_var: False}):
            return True
        
        return False
    
    def geometric_entropy(cnf):
        n = len(cnf[0])
        box_count = 0
        scale = 1.0
        while True:
            count = 0
            for i in range(-int(scale), int(scale) + 1):
                for j in range(-int(scale), int(scale) + 1):
                    if all(x * (i + j) <= 0 for x in cnf[0]):
                        count += 1
            box_count += count
            scale *= 2
            if scale > 100:
                break
        return math.log(box_count, 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        entropy = geometric_entropy(cnf)
        width = dpll(cnf)
        results.append((n, entropy, width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    entropies = [r[1] for r in results]
    widths = [r[2] for r in results]
    correlation_coefficient = sum((e - sum(entropies) / len(entropies)) * (w - sum(widths) / len(widths)) for e, w in zip(entropies, widths)) / (len(results) * math.sqrt(sum((e - sum(entropies) / len(entropies))**2 for e in entropies)) * math.sqrt(sum((w - sum(widths) / len(widths))**2 for w in widths)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient >= 0.8 else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")