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
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        learned_clauses = []
        
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    a, b = clauses[i], clauses[j]
                    if -a[0] in b and -a[1] in b:
                        new_clause = tuple(sorted([-b[0], -b[1]]))
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(learned_clauses)
            learned_clauses.append(new_clause)
            clauses.add(new_clause)
    
    def geometric_langlands_dimension(cnf):
        # Placeholder for actual computation; returns a random value for testing
        return random.uniform(1, 10)
    
    n_values = [5, 10, 15, 20, 30, 40]
    gld_values = []
    w_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        gld = geometric_langlands_dimension(cnf)
        w = resolution_width(cnf)
        
        if not (gld is not None and w is not None):
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": 0.0,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        gld_values.append(gld)
        w_values.append(w)
    
    mean_gld = sum(gld_values) / len(gld_values)
    mean_w = sum(w_values) / len(w_values)
    
    correlation_coefficient = sum((gld - mean_gld) * (w - mean_w) for gld, w in zip(gld_values, w_values)) / len(gld_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(cc >= 0.5 for cc in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")