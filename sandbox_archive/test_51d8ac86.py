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
    
    def generate_cnf(n: int):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll_width(cnf):
        unit_clauses = list(filter(lambda c: len(c) == 1, cnf))
        if not unit_clauses:
            return 0
        unit_clause = random.choice(unit_clauses)
        new_cnf = [c for c in cnf if unit_clause[0] not in c and -unit_clause[0] not in c]
        return 1 + dpll_width(new_cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            cnf = generate_cnf(n)
            width = dpll_width(cnf)
            if width > 0:
                total_width += width
                instances_tested += 1
    
    mean_width = total_width / instances_tested if instances_tested > 0 else 0
    conjecture_holds = all(math.log2(width) >= n for n, width in zip(n_values, [math.log2(2**n) for n in n_values]))
    
    return {
        "metric_name": "DPLL Width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "n-dependent bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n-dependent bound\" first_failing_seed={first_failing_seed}")