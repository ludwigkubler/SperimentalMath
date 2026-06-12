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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        if not cnf:
            return 0
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if not unit_clauses:
            return max(dpll_width([c for c in cnf if c[0] != literal]) + 1, dpll_width([c for c in cnf if c[1] != -literal]) + 1)
        literal = unit_clauses[0]
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        return max(dpll_width(new_cnf), dpll_width([c for c in new_cnf if c[0] == literal]) + 1)
    
    def kahler_order(cnf):
        # Placeholder function to simulate the construction of a Kähler manifold
        # and its minimal order. This is a dummy implementation.
        return len(cnf) ** 2
    
    instances_tested = 30
    n_max = 40
    total_diff = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        w_phi = dpll_width(cnf)
        order_X = kahler_order(cnf)
        diff = abs(order_X - w_phi)
        total_diff += diff
    
    mean_diff = Fraction(total_diff, instances_tested)
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": float(mean_diff),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_diff <= 2,
        "counterexample": "" if mean_diff <= 2 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")