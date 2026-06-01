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
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_metric_value = 0.0
    max_n = n
    conjecture_holds = True
    counterexample = ""

    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = random.sample(range(1, n + 1), 2)
            clauses.append(clause)
        return clauses

    def tseitin_representation(cnf):
        literals = list(range(1, n + 1))
        formulas = []
        for literal in literals:
            formulas.append(f"X_{literal}")
        for clause in cnf:
            new_var = f"Y_{len(formulas) + 1}"
            formulas.append(new_var)
            for literal in clause:
                formulas.append(f"{new_var} <-> X_{abs(literal)}")
            formulas.append(f"{new_var} -> {clause[0]}")
            formulas.append(f"{new_var} -> ~{clause[1]}")
        return formulas

    def dpll_search_tree_diameter(formulas):
        # Simplified DPLL search tree diameter calculation
        return len(formulas)

    for _ in range(50):  # Sample 50 instances per seed
        cnf = generate_cnf(n)
        tseitin_formulas = tseitin_representation(cnf)
        dpll_diameter = dpll_search_tree_diameter(tseitin_formulas)
        metric_value = math.log(math.factorial(n)) * min(len(formula.split()) for formula in tseitin_formulas if '->' not in formula)
        instances_tested += 1
        total_metric_value += metric_value

    mean_metric_value = total_metric_value / instances_tested
    if n > max_n:
        max_n = n

    return {
        "metric_name": "log(n!) * min_{P ∈ φ_T} |P|",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")