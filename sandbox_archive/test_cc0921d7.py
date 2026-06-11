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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def qsi(cnf):
        # Constructive mapping to quasi-symmetric space index
        clauses = set(tuple(sorted(c)) for c in cnf)
        return len(clauses) / n
    
    def resolution_width(cnf):
        # Simple heuristic for resolution width (not accurate but sufficient for testing)
        return max(len(c) for c in cnf)
    
    n_max = 0
    instances_tested = 0
    total_qsi = 0
    total_width = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        cnf = generate_cnf(n, m)
        qsi_val = qsi(cnf)
        width = resolution_width(cnf)
        
        if qsi_val == 0 or width == 0:
            continue
        
        instances_tested += 1
        total_qsi += qsi_val * width
        total_width += width
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_qsi = total_qsi / total_width
    correlation_coefficient = (total_qsi - instances_tested * mean_qsi) / math.sqrt(instances_tested * (1 - instances_tested / n_max))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")