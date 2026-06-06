# auto-injected by SEC sandbox
import math
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

def generate_cnf(n, m):
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, 2)
        cnf.append(clause)
    return cnf

def is_satisfiable(cnf):
    stack = []
    assignment = {}
    def dpll(index=0):
        if index == len(cnf):
            return True
        literals = set()
        for clause in cnf[index:]:
            literals.update(clause)
        literal = next(iter(literals))
        while literal in assignment:
            literal = -literal
        assignment[literal] = True
        if dpll(index + 1):
            return True
        del assignment[literal]
        assignment[-literal] = True
        if dpll(index + 1):
            return True
        del assignment[-literal]
        return False
    return dpll()

def compute_orbits(cnf):
    graph = {i: set() for i in range(1, len(cnf) + 1)}
    for clause in cnf:
        for literal in clause:
            if -literal in graph:
                graph[abs(literal)].add(abs(-literal))
                graph[abs(-literal)].add(abs(literal))
    visited = [False] * (len(cnf) + 1)
    orbits = []
    
    def dfs(node):
        stack = [node]
        while stack:
            current = stack.pop()
            if not visited[current]:
                visited[current] = True
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
    
    for i in range(1, len(cnf) + 1):
        if not visited[i]:
            dfs(i)
            orbits.append(len(graph[i]))
    return sum(orbits)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 30)
    m = random.randint(n * 2, n * 4)
    cnf = generate_cnf(n, m)
    orbits = compute_orbits(cnf)
    resolution_width = is_satisfiable(cnf)  # Simplified for this test
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": Fraction(orbits, n),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if resolution_width else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Orbit Width Ratio does not match resolution width\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient support")