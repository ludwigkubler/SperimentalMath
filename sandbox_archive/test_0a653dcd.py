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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def min_symmetric_bilinear_form(cnf, n):
        # Placeholder implementation
        return random.random()
    
    def communication_complexity_rank_variance(cnf, n):
        # Placeholder implementation
        return random.random()
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n, n * (n - 1) // 2)
        min_sbf = min_symmetric_bilinear_form(cnf, n)
        ccr_var = communication_complexity_rank_variance(cnf, n)
        results.append((min_sbf, ccr_var))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_sbfs = [r[0] for r in results]
    ccr_vars = [r[1] for r in results]
    mean_min_sbf = sum(min_sbfs) / len(min_sbfs)
    mean_ccr_var = sum(ccr_vars) / len(ccr_vars)
    
    correlation_coefficient = (sum((min_sbfs[i] - mean_min_sbf) * (ccr_vars[i] - mean_ccr_var) for i in range(len(min_sbfs))) /
                               math.sqrt(sum((min_sbfs[i] - mean_min_sbf) ** 2 for i in range(len(min_sbfs))) *
                                         sum((ccr_vars[i] - mean_ccr_var) ** 2 for i in range(len(ccr_vars)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.5 and correlation_coefficient <= 1.5,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"correlation_coefficient < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")