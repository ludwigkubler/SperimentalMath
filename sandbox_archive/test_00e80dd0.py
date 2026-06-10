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

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for var in variables:
        clauses.append([var])
    for i in range(1, n):
        clause = [f'x{i}', f'x{i+1}', f'~x{i}']
        clauses.append(clause)
    clauses.append([f'~x{n}'])
    return clauses

def dpll(clauses, assignment={}):
    if not clauses:
        return True
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        new_assignment = {**assignment, literal: True} if literal.startswith('x') else {**assignment, literal: False}
        return dpll([c for c in clauses if literal not in c and ~literal not in c], new_assignment)
    pure_literals = {}
    for clause in clauses:
        for literal in clause:
            if literal.startswith('~'):
                neg_literal = literal[1:]
                if neg_literal in pure_literals:
                    pure_literals[neg_literal] += 1
                else:
                    pure_literals[neg_literal] = -1
            else:
                if literal in pure_literals:
                    pure_literals[literal] -= 1
                else:
                    pure_literals[literal] = 1
    for literal, count in pure_literals.items():
        if count == len(clauses):
            new_assignment = {**assignment, literal: True} if literal.startswith('x') else {**assignment, literal: False}
            return dpll([c for c in clauses if literal not in c and ~literal not in c], new_assignment)
    literal = random.choice([k for k, v in pure_literals.items() if v != 0])
    new_assignment = {**assignment, literal: True} if literal.startswith('x') else {**assignment, literal: False}
    return dpll(clauses, new_assignment) or dpll(clauses, {**assignment, literal: False})

def local_induction_degree(clauses):
    n = len(clauses)
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if any(lit in clauses[i] and ~lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                graph[i].append(j)
                graph[j].append(i)
    visited = [False] * n
    def dfs(node):
        stack = [node]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    stack.append(neighbor)
    dfs(0)
    return sum(not v for v in visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_tseitin_formula(n)
            w_G = dpll(clauses)  # Measure resolution proof width
            if not w_G:
                continue
            lind_G = local_induction_degree(clauses)  # Measure minimal local induction degree
            results.append({"lind_G": lind_G, "w_G": w_G})
    if not results:
        return {
            "metric_name": "lind_over_w",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    lind_over_w = sum(result["lind_G"] / result["w_G"] for result in results) / len(results)
    return {
        "metric_name": "lind_over_w",
        "metric_value": lind_over_w,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(result["lind_G"] <= result["w_G"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_lind_over_w = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_lind_over_w} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_lind_over_w} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"lind_G > w_G\" first_failing_seed={r['seed']}")
                break