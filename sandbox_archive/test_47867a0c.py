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
    
    def min_local_ring_norm(phi):
        p = 2  # Using a fixed p-adic field for simplicity
        valuation = lambda clause: max([abs(int(lit)) % p for lit in clause], default=0)
        return sum(valuation(clause) for clause in phi) / len(phi)

    def resolution_width(phi):
        stack = [phi]
        while stack:
            clause = stack.pop()
            if not any(lit in clause for lit in clause):
                continue
            literal = random.choice([lit for lit in clause if lit != 0])
            new_clauses = []
            for c in phi:
                if literal in c:
                    new_clauses.append([l for l in c if l != literal and l != -literal])
                elif -literal in c:
                    continue
                else:
                    new_clauses.append(c)
            stack.extend(new_clauses)
        return len(phi)

    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(lit == 0 for lit in clause):
                continue
            clauses.append(clause)
        return clauses

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_cnf(n)
        min_norm_val = min_local_ring_norm(phi)
        width_val = resolution_width(phi)
        results.append({"n": n, "min_norm": min_norm_val, "width": width_val})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    min_norms = [result["min_norm"] for result in results]
    widths = [result["width"] for result in results]
    
    mean_min_norm = sum(min_norms) / len(min_norms)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = sum((min_norm - mean_min_norm) * (width - mean_width) for min_norm, width in zip(min_norms, widths)) / (len(results) * math.sqrt(sum((min_norm - mean_min_norm)**2 for min_norm in min_norms)) * math.sqrt(sum((width - mean_width)**2 for width in widths)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    if not all("metric_value" in r and r["metric_value"] is not None for r in results):
        print("RESULT: INCONCLUSIVE reason=missing_metric_values")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] < 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std=NA support_fraction={support_fraction:.2f}")
        elif any(r["metric_value"] < 0.5 for r in results):
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if r["metric_value"] < 0.5)
            print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
        else:
            print(f"RESULT: INCONCLUSIVE reason=mean_correlation_too_low mean_corr={mean_corr:.2f}")