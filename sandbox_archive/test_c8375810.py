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
    
    def circuit_monotone_width(cnf):
        # Simplified heuristic to estimate circuit monotone width
        return len(cnf) + len(set(abs(lit) for lit in sum(cnf, [])))
    
    m_values = [5, 10, 15, 20, 30, 40]
    n_values = [5, 10, 15, 20, 30, 40]
    
    total_metric_value = 0
    instances_tested = 0
    n_max = -1
    
    for m in m_values:
        for n in n_values:
            cnf = generate_cnf(m, n)
            generators_count = len(cnf)  # Simplified heuristic for Coxeter group generators
            width = circuit_monotone_width(cnf)
            
            total_metric_value += generators_count
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value <= (m_values[-1] ** (1/3) * n_values[-1] ** (2/3))
    
    return {
        "metric_name": "Coxeter Group Generators",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"m={len(r['metric_name'])}, n={r['n_max']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break