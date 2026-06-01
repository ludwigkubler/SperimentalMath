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

    def resolution_width(cnf):
        stack = cnf[:]
        while True:
            unit_clauses = [c for c in stack if len(c) == 1]
            if not unit_clauses:
                break
            u = unit_clauses[0][0]
            new_clause = []
            for clause in stack:
                if u in clause:
                    continue
                if -u in clause:
                    new_clause.extend([x for x in clause if x != -u])
                else:
                    new_clause.append(x)
            stack.remove(u)
            stack.extend(new_clause)
        return len(stack)

    def l_function(cnf):
        n = len(cnf[0]) // 2
        characteristic_poly = [1]
        for _ in range(n):
            new_poly = [0] * (len(characteristic_poly) + 1)
            for i in range(len(characteristic_poly)):
                new_poly[i+1] += characteristic_poly[i]
            characteristic_poly = new_poly
        return characteristic_poly

    def minimal_order(l_function):
        n = len(l_function)
        if l_function[0] == 0:
            return None
        order = 0
        for i in range(1, n):
            if l_function[i] != 0:
                order += 1
        return order

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def hecke_eigenform_order(l_function):
        n = len(l_function)
        if l_function[0] == 0:
            return None
        order = 1
        for i in range(1, n):
            if l_function[i] != 0:
                order = lcm(order, i + 1)
        return order

    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))

    n_values = [5, 10, 15, 20, 30, 40]
    order_values = []
    width_values = []

    for n in n_values:
        cnf = generate_cnf(n)
        l_func = l_function(cnf)
        hecke_order = hecke_eigenform_order(l_func)
        if hecke_order is not None:
            order_values.append(hecke_order)
            width_values.append(resolution_width(cnf))

    if len(order_values) < 30 or len(width_values) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(order_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }

    corr = correlation(order_values, width_values)
    return {
        "metric_name": "Correlation",
        "metric_value": corr,
        "instances_tested": len(order_values),
        "n_max": max(n_values),
        "conjecture_holds": corr > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = "SUPPORTED"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Insufficient data to refute"
        mean_corr = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        result = "FALSIFIED"

    print(f"RESULT: {result} mean={mean_corr} std=0.0 support_fraction={support_fraction}")