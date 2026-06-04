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
            clauses.append(clause)
        return clauses

    def p_adic_diff(cnf, p, i):
        # Constructive mapping to compute p-adic differential
        # This is a placeholder implementation; replace with actual logic
        return 0

    def resolution_width(cnf):
        # Placeholder for resolution proof width calculation
        return random.randint(1, 10)

    n = 5 + (seed % 26) * 5  # Ensure n_min >= 5 and n_max >= 20
    cnf = generate_cnf(n)
    
    min_p_adic_diff = float('inf')
    for p in range(2, n):
        for i in range(1, n):
            diff = p_adic_diff(cnf, p, i)
            if abs(diff) < min_p_adic_diff:
                min_p_adic_diff = abs(diff)

    width = resolution_width(cnf)
    
    return {
        "metric_name": "min_p_adic_diff",
        "metric_value": min_p_adic_diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,  # Placeholder; replace with actual logic
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")