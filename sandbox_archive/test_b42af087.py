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
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            cnf.append(clause)
        return cnf
    
    def automorphism_group_order(cnf):
        n = len(cnf[0])
        aut_order = 1
        for perm in itertools.permutations(range(n)):
            if all(all(cnf[i][j] == cnf[i][perm[j]] for j in range(n)) for i in range(len(cnf))):
                aut_order += 1
        return aut_order
    
    def circuit_monotone_width(cnf):
        n = len(cnf[0])
        width = [0] * n
        for clause in cnf:
            max_var = max(abs(var) for var in clause)
            for i in range(max_var):
                if any(clause[j] == -i+1 or clause[j] == i+1 for j in range(n)):
                    width[i] += 1
        return max(width)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        aut_order = automorphism_group_order(cnf)
        w_m = circuit_monotone_width(cnf)
        results.append((aut_order, w_m))
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    aut_orders = [r[0] for r in results]
    w_ms = [r[1] for r in results]
    mean_aut_order = sum(aut_orders) / len(aut_orders)
    mean_w_m = sum(w_ms) / len(w_ms)
    correlation_coefficient = (sum((aut_orders[i] - mean_aut_order) * (w_ms[i] - mean_w_m) for i in range(len(results))) /
                                math.sqrt(sum((aut_orders[i] - mean_aut_order)**2 for i in range(len(results))) *
                                          sum((w_ms[i] - mean_w_m)**2 for i in range(len(results)))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(aut_orders),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.8 and all(abs(a - w) <= 3 for a, w in zip(aut_orders, w_ms)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")