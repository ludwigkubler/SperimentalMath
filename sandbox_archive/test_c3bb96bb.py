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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y
    
    def gcd_list(lst):
        result = lst[0]
        for num in lst:
            result = gcd(result, num)
        return result
    
    def lcm_list(lst):
        result = lst[0]
        for num in lst:
            result = lcm(result, num)
        return result
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def incidence_polytope(cnf):
        n = len(cnf[0])
        vertices = []
        for assignment in [list(x) for x in itertools.product([0, 1], repeat=n)]:
            if all(any(assignment[i-1] == abs(lit) for lit in clause) for clause in cnf):
                vertices.append(tuple(assignment))
        return vertices
    
    def minimal_ehrhart_quotient(vertices):
        n = len(vertices[0])
        volume = 1
        for i in range(n):
            min_val = min(vertex[i] for vertex in vertices)
            max_val = max(vertex[i] for vertex in vertices)
            volume *= (max_val - min_val + 1)
        return volume
    
    def circuit_monotone_width(cnf):
        n = len(cnf[0])
        stack = []
        for clause in cnf:
            for lit in clause:
                if not stack or stack[-1] != -lit:
                    stack.append(lit)
                else:
                    stack.pop()
        return len(stack)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    def is_valid_cnf(cnf):
        for clause in cnf:
            if not any(lit != 0 for lit in clause):
                return False
        return True
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    while not is_valid_cnf(cnf):
        cnf = generate_cnf(n)
    
    vertices = incidence_polytope(cnf)
    mu = minimal_ehrhart_quotient(vertices)
    w_m = circuit_monotone_width(cnf)
    
    if mu == 0 or w_m == 0:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    corr = pearson_correlation([mu], [w_m])
    holds_bound = mu**2 <= w_m
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": corr,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": corr >= 0.5 and holds_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")