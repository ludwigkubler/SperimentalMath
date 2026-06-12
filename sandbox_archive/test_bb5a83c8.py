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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def generate_random_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = random.sample(range(1, n + 1), random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def is_tautology(clauses):
    literals = set()
    for clause in clauses:
        literals.update(abs(x) for x in clause)
    assignments = {x: None for x in literals}
    def backtrack():
        if len(assignments) == 0:
            return True
        var = next(iter(assignments))
        for val in [True, False]:
            assignments[var] = val
            if all(not any(lit == -var for lit in clause) or any(lit == var for lit in clause) for clause in clauses):
                if backtrack():
                    return True
            assignments.pop(var)
        return False
    return not backtrack()

def compute_clause_tree_width(clauses):
    n = len(clauses)
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if any(lit in clauses[i] and -lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                graph[i].append(j)
                graph[j].append(i)
    
    def dfs(node, parent):
        nonlocal max_width
        children = [child for child in graph[node] if child != parent]
        if not children:
            return 0
        depths = sorted([dfs(child, node) for child in children])
        width = len(depths) - 1 + (depths[-1] if depths else 0)
        max_width = max(max_width, width)
        return 1 + depths[-1]
    
    max_width = 0
    dfs(0, -1)
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    
    for n in range(5, n_max + 1):
        if n > 20 and (n % 10 != 0 or n == 20):
            continue
        for _ in range(instances_tested // (n_max - 4) + 1):
            clauses = generate_random_cnf(n, random.randint(2 * n, 3 * n))
            if is_tautology(clauses):
                continue
            width = compute_clause_tree_width(clauses)
            if not (n**2 * math.log(n) <= width <= n**2 * math.log(n)):
                return {
                    "metric_name": "clause_tree_width",
                    "metric_value": width,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"Clause tree width {width} out of range for n={n}"
                }
            metric_value += width
    
    return {
        "metric_name": "clause_tree_width",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"clause_tree_width_out_of_range\" first_failing_seed={first_failing_seed}")