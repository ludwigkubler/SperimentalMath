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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def norm(cnf):
        m = len(cnf)
        n = max(abs(lit) for lit in sum(cnf, []))
        return (math.log(m + n)) ** 2
    
    def resolution_length(cnf):
        # Simplified estimation of resolution length
        return len(cnf) * math.log(len(cnf), 2)
    
    m_values = [5, 10, 15, 20, 30, 40]
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        for n in n_values:
            cnf = generate_cnf(m, n)
            N_phi = norm(cnf)
            res_length = resolution_length(cnf)
            results.append((N_phi, res_length))
    
    if not results:
        return {
            "metric_name": "norm_vs_resolution",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    N_phi_avg = sum(N for N, _ in results) / len(results)
    res_length_avg = sum(res for _, res in results) / len(results)
    correlation = sum((N - N_phi_avg) * (res - res_length_avg) for N, res in results) / len(results)
    
    lower_bound = 0.95 * N_phi_avg
    upper_bound = 1.1 * N_phi_avg
    
    conjecture_holds = all(lower_bound <= N <= upper_bound for N, _ in results) and correlation > 0
    counterexample = "" if conjecture_holds else "correlation_negative"
    
    return {
        "metric_name": "norm_vs_resolution",
        "metric_value": res_length_avg,
        "instances_tested": len(results),
        "n_max": max(n for _, n in m_values + n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] and "correlation_negative" in r["counterexample"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_negative\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'] and 'correlation_negative' in result['counterexample'])}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_evidence")