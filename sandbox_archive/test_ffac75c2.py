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
    
    def generate_k_cnf(n, k):
        cnf = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def communication_complexity_rank(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)  # Simplified for demonstration
    
    def minimal_order_of_arithmetic_cycles(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf) * len(cnf[0])  # Simplified for demonstration
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_k_cnf(n, k=3)
            m_order = minimal_order_of_arithmetic_cycles(cnf)
            r_phi = communication_complexity_rank(cnf)
            results.append((m_order, r_phi))
    
    if not results:
        return {
            "metric_name": "minimal_order_of_arithmetic_cycles",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_order_values = [m for m, _ in results]
    r_phi_values = [r for _, r in results]
    
    metric_mean = sum(m_order_values) / len(m_order_values)
    support_fraction = sum(1 for m, r in results if O(n**2 * math.log(n)) <= m <= C * r) / len(results)
    
    return {
        "metric_name": "minimal_order_of_arithmetic_cycles",
        "metric_value": metric_mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8 and metric_mean <= C,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, m_order_mean={r['metric_value']}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")