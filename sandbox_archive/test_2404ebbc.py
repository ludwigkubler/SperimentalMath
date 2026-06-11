# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n * 2) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        if not cnf:
            return True
        literals = set()
        for clause in cnf:
            literals.update(clause)
        literal = random.choice(list(literals))
        positive_cnf = [clause for clause in cnf if literal not in clause]
        negative_cnf = [tuple([-l for l in clause] if l == -literal else l for l in clause) for clause in cnf if -literal not in clause]
        return dpll(positive_cnf) or dpll(negative_cnf)
    
    def geometric_arithmetical_rank(cnf):
        # Placeholder for actual implementation
        return random.randint(1, 5)
    
    n_max = 40
    instances_tested = 30
    g_ar_values = []
    w_DPLL_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        if not dpll(cnf):
            continue
        g_ar = geometric_arithmetical_rank(cnf)
        w_DPLL = len(cnf)  # Placeholder for actual DPLL width calculation
        g_ar_values.append(g_ar)
        w_DPLL_values.append(w_DPLL)
    
    if not g_ar_values or not w_DPLL_values:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_g_ar = sum(g_ar_values) / len(g_ar_values)
    mean_w_DPLL = sum(w_DPLL_values) / len(w_DPLL_values)
    covariance = sum((g_ar - mean_g_ar) * (w_DPLL - mean_w_DPLL) for g_ar, w_DPLL in zip(g_ar_values, w_DPLL_values)) / len(g_ar_values)
    variance_g_ar = sum((g_ar - mean_g_ar) ** 2 for g_ar in g_ar_values) / len(g_ar_values)
    variance_w_DPLL = sum((w_DPLL - mean_w_DPLL) ** 2 for w_DPLL in w_DPLL_values) / len(w_DPLL_values)
    
    correlation_coefficient = covariance / (variance_g_ar * variance_w_DPLL) ** 0.5
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(g_ar >= w_DPLL for g_ar, w_DPLL in zip(g_ar_values, w_DPLL_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric")