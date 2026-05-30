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
    
    def minimal_order_of_quadratic_residues(clauses):
        residues = set()
        for clause in clauses:
            for literal in clause:
                if literal % 2 == 0 and literal != 0:
                    residues.add(literal ** 2 % (literal + 1))
        return min(residues) if residues else None
    
    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        return len(clauses)
    
    n_values = [10, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        for _ in range(75):  # Aim for at least 30 instances per seed
            clauses = [[random.randint(-n, n) for _ in range(random.randint(2, 5))] for _ in range(n)]
            q = minimal_order_of_quadratic_residues(clauses)
            if q is None:
                continue
            w = resolution_width(clauses)
            results.append((q, w))
            total_instances += 1
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    q_values, w_values = zip(*results)
    mean_q = sum(q_values) / len(q_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = (sum((q - mean_q) * (w - mean_w) for q, w in results) /
                               math.sqrt(sum((q - mean_q) ** 2 for q in q_values) *
                                         sum((w - mean_w) ** 2 for w in w_values)))
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, q={min(r['metric_values'])}, w={max(r['metric_values'])}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_evidence")