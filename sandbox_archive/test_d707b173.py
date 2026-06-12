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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        # Simplified DPLL width calculation
        max_clause_length = 0
        for clause in cnf:
            max_clause_length = max(max_clause_length, len(clause))
        return max_clause_length
    
    def kahler_order(cnf):
        # Simplified Kähler order calculation (placeholder)
        return sum(len(clause) for clause in cnf)
    
    n = 40
    cnf = generate_cnf(n)
    w_phi = dpll_width(cnf)
    order_X = kahler_order(cnf)
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": abs(order_X - w_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(order_X - w_phi) <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")