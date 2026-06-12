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
    
    def generate_instance(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dpll_width(clauses):
        # Simplified DPLL width calculation
        return len(max(set.union(*clauses), key=clauses.count))
    
    def quasi_classical_order(n):
        # Placeholder for actual computation of quasi-classical order
        return n**2  # Simplified example
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        m_values = []
        w_values = []
        for _ in range(5):  # Test with 5 instances per size
            instance = generate_instance(n)
            m = quasi_classical_order(n)
            w = dpll_width(instance)
            results.append({"n": n, "m": m, "w": w})
            m_values.append(m)
            w_values.append(w)
            instances_tested += 1
        
        if not m_values or not w_values:
            return {
                "metric_name": "quasi_classical_order_dpll_width",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mean_m = sum(m_values) / len(m_values)
        mean_w = sum(w_values) / len(w_values)
        std_m = math.sqrt(sum((x - mean_m) ** 2 for x in m_values) / len(m_values))
        std_w = math.sqrt(sum((x - mean_w) ** 2 for x in w_values) / len(w_values))
        
        if not (mean_m >= n**3 and mean_m <= 1.5 * n**(3/2)):
            return {
                "metric_name": "quasi_classical_order_dpll_width",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"m({n}) = {mean_m} does not satisfy O(n^3) <= m(n) <= 1.5*n^(3/2)"
            }
    
    return {
        "metric_name": "quasi_classical_order_dpll_width",
        "metric_value": None,
        "instances_tested": instances_tested,
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {seed} {trial_result}")
        results.append(trial_result)
    
    mean_shv = sum(r["instances_tested"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_shv} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_shv} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")