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
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def solve(model):
        if not cnf:
            return model
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_model = {**model, abs(literal): literal > 0}
            return solve([c for c in cnf if literal not in c and -literal not in c], new_model)
        pure_literal = next((l for l in variables if all(l not in clause or -l not in clause for clause in cnf)), None)
        if pure_literal is None:
            return None
        new_model = {**model, abs(pure_literal): pure_literal > 0}
        return solve([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_model)
    variables = list(range(1, len(cnf) + 1))
    return solve({})

def minimal_order_p_adic(n):
    p = 2
    while True:
        # Compute the order of a cyclic p-adic number in the extension of F_{2^n}
        order = n * math.log(p, 2)
        if order.is_integer():
            return int(order)
        p += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        depth = dpll(cnf)
        if depth is None:
            continue
        p_adic_order = minimal_order_p_adic(n)
        results.append((depth, p_adic_order))
    if not results:
        return {
            "metric_name": "Circuit Depth vs. P-Adic Order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid CNF generated"
        }
    depths, p_adic_orders = zip(*results)
    correlation_coefficient = sum((d - mean_depth) * (p - mean_p_adic_order) for d, p in zip(depths, p_adic_orders)) / math.sqrt(sum((d - mean_depth) ** 2 for d in depths) * sum((p - mean_p_adic_order) ** 2 for p in p_adic_orders))
    return {
        "metric_name": "Circuit Depth vs. P-Adic Order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(depths),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")