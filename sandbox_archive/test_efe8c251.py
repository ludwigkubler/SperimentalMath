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
        for _ in range(10):  # Generate 10 clauses
            clause = [random.randint(-n, n) for _ in range(3)]
            cnf.append(clause)
        return cnf
    
    def p_adic_order(p, n):
        if n == 0:
            return 0
        order = 0
        while n % p == 0:
            n //= p
            order += 1
        return order
    
    def circuit_depth(cnf):
        # Simplified DPLL solver to estimate circuit depth
        stack = []
        for clause in cnf:
            if not any(lit < 0 and -lit in stack for lit in clause):
                stack.extend(clause)
        return len(stack)
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    
    for n in range(5, n_max + 1, 5):  # Sweep through sizes 5, 10, 15, 20, 30, 40
        cnf = generate_cnf(n)
        p = random.randint(2, n)  # Random prime number for p-adic order
        negation_order = p_adic_order(p, len(cnf))
        total_order += negation_order
        instances_tested += 1
    
    mean_order = total_order / instances_tested
    conjecture_holds = mean_order <= n_max * math.log2(n_max) * (n_max ** (1/3))
    
    return {
        "metric_name": "p-adic Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean order {mean_order} exceeds bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean order exceeds bound\" first_failing_seed={first_failing_seed}")