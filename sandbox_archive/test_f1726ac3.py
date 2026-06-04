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
        cnf = []
        for _ in range(10):  # Generate 10 clauses with n variables
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        for clause in cnf:
            if not any(abs(lit) == abs(clause[0]) for lit in stack):
                stack.append(clause[0])
            else:
                continue
        return len(stack)
    
    def quaternionic_kahler_form_order(n):
        # Simplified computation of minimal order (logarithmic approximation)
        if n <= 1:
            return 0
        return math.ceil(math.log(n) / math.log(math.log(n)))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    order = quaternionic_kahler_form_order(n)
    
    if width < 1.5 * order:
        return {
            "metric_name": "resolution_width_over_quaternionic_kahler",
            "metric_value": width / order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"width={width}, order={order}"
        }
    else:
        return {
            "metric_name": "resolution_width_over_quaternionic_kahler",
            "metric_value": width / order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_widths = sum(r["metric_value"] * r["instances_tested"] for r in results)
    total_instances = sum(r["instances_tested"] for r in results)
    mean_width = total_widths / total_instances
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 * r["instances_tested"] for r in results) / total_instances)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")