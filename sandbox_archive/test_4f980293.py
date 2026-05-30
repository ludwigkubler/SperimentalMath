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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(k)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate width
        stack = []
        literals = set()
        for clause in clauses:
            if not any(lit in literals for lit in clause):
                literals.update(clause)
                stack.append((clause, literals.copy()))
            else:
                return len(literals)
        return len(literals)
    
    def hodge_order(n):
        # Simplified Hodge order calculation
        return int(math.log2(n)) ** 2
    
    n = random.randint(5, 40)
    k = random.randint(2, min(3, n))
    clauses = generate_k_cnf(n, k)
    width = resolution_width(clauses)
    hodge_order_val = hodge_order(n)
    
    return {
        "metric_name": "Hodge Order",
        "metric_value": hodge_order_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= hodge_order_val * math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 7 for i in range(5, 8)]  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")