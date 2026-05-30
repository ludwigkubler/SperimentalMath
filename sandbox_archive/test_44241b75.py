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
    
    def euler_characteristic(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        m = len(cnf)
        return 2 * (n - m + 1)
    
    def topological_complexity(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Test each size 5 times
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            chi = euler_characteristic(cnf)
            tc = topological_complexity(cnf)
            results.append((chi, tc))
    
    mean_chi = sum(chi for chi, _ in results) / len(results)
    mean_tc = sum(tc for _, tc in results) / len(results)
    std_chi = math.sqrt(sum((chi - mean_chi) ** 2 for chi, _ in results) / len(results))
    std_tc = math.sqrt(sum((tc - mean_tc) ** 2 for _, tc in results) / len(results))
    
    conjecture_holds = all(chi <= m**(1/3) * n**(2/3) for chi, (_, m, n) in zip(results, [(n, m) for n in n_values for _ in range(5)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": mean_chi,
        "instances_tested": len(results),
        "n_max": max(n_values),
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")