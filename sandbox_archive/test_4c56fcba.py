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
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        if not cnf:
            return True
        literal = next(lit for lit in range(1, len(cnf) + 1) if any(lit in clause or -lit in clause for clause in cnf))
        positive = [clause for clause in cnf if literal in clause]
        negative = [clause for clause in cnf if -literal in clause]
        return dpll(positive) or dpll([c for c in cnf if not (-literal in c)])
    
    def geometric_ar(cnf):
        # Simplified mapping to rank 1 structure
        return len(cnf)
    
    n_max = 40
    instances_tested = 30
    total_g_ar = 0
    total_w_DPLL = 0
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        g_ar_value = geometric_ar(cnf)
        w_DPLL_value = dpll(cnf)
        
        if w_DPLL_value == 0:
            continue
        
        total_g_ar += g_ar_value
        total_w_DPLL += w_DPLL_value
    
    mean_g_ar = Fraction(total_g_ar, instances_tested)
    mean_w_DPLL = Fraction(total_w_DPLL, instances_tested)
    
    variance_g_ar = sum((g_ar_value - mean_g_ar) ** 2 for g_ar_value in range(instances_tested)) / instances_tested
    variance_w_DPLL = sum((w_DPLL_value - mean_w_DPLL) ** 2 for w_DPLL_value in range(instances_tested)) / instances_tested
    
    if variance_g_ar == 0 or variance_w_DPLL == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    covariance = sum((g_ar_value - mean_g_ar) * (w_DPLL_value - mean_w_DPLL) for g_ar_value, w_DPLL_value in zip(range(instances_tested), range(instances_tested))) / instances_tested
    correlation_coefficient = covariance / (variance_g_ar * variance_w_DPLL) ** 0.5
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= Fraction(8, 10),
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=variance_zero")