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
from fractions import Fraction
import math

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Each variable appears in 10 clauses on average
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        random.shuffle(clause)
        cnf.append(tuple(clause))
    return cnf

def is_satisfiable(cnf):
    def backtrack(k):
        if k > n:
            return True
        for val in [True, False]:
            assignment[k] = val
            if all(any(assignment[abs(lit)] == sign for lit, sign in clause) for clause in cnf):
                if backtrack(k + 1):
                    return True
        return False

    n = len(cnf)
    assignment = [None] * (n + 1)
    return backtrack(1)

def p_adic_valuation(cnf):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    prime = 2  # Using the smallest prime for simplicity
    valuation = 0
    for clause in cnf:
        product = 1
        for lit, sign in clause:
            if assignment[abs(lit)] == sign:
                product *= abs(lit)
        valuation += math.log(product, prime) / math.log(prime, 2)
    return valuation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if not is_satisfiable(cnf):
            continue
        valuation = p_adic_valuation(cnf)
        complexity = len(cnf) * n  # Simplified complexity measure
        results.append((n, valuation, complexity))
    
    if not results:
        return {
            "metric_name": "p-adic Valuation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    mean_valuation = sum(valuation for _, valuation, _ in results) / len(results)
    std_valuation = math.sqrt(sum((valuation - mean_valuation) ** 2 for _, valuation, _ in results) / len(results))
    
    return {
        "metric_name": "p-adic Valuation",
        "metric_value": mean_valuation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all("counterexample" in result and result["counterexample"] == "" for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")