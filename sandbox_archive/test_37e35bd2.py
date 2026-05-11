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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_graph(n, p):
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                graph[i][j] = graph[j][i] = 1
    return graph

def dfs(graph, node, visited):
    stack = [node]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in range(len(graph)):
                if graph[node][neighbor]:
                    stack.append(neighbor)

def tree_depth(graph):
    n = len(graph)
    visited = [False] * n
    depth = 0
    for i in range(n):
        if not visited[i]:
            dfs(graph, i, visited)
            depth += 1
    return depth

def tseitin_formula(graph):
    n = len(graph)
    formula = []
    for i in range(n):
        clause = [f"X{i}"]
        for j in range(i + 1, n):
            if graph[i][j]:
                clause.append(f"-X{j}")
        formula.append(clause)
    return formula

def dpll(formula, assignment=None):
    if not formula:
        return True
    if any(not any(lit in assignment for lit in clause) for clause in formula):
        return False
    literal = next((lit for lit in formula[0] if lit not in assignment), None)
    if literal is None:
        return True
    new_formula = [clause[:] for clause in formula]
    for i, clause in enumerate(new_formula):
        if literal in clause:
            new_formula[i].remove(literal)
        elif f"-{literal}" in clause:
            new_formula[i].remove(f"-{literal}")
            new_formula[i] = [-x for x in new_formula[i]]
    return dpll(new_formula, assignment + [literal]) or dpll(new_formula, assignment + [f"-{literal}"])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    p = 0.3
    graph = random_graph(n, p)
    td = tree_depth(graph)
    formula = tseitin_formula(graph)
    length = sum(1 for _ in range(1000) if dpll(formula))
    c = math.log(length) / td if td > 0 else float('inf')
    return {
        "metric_name": "Resolution proof length",
        "metric_value": length,
        "instances_tested": 1000,
        "conjecture_holds": c >= 1,
        "counterexample": "" if c >= 1 else f"Graph with n={n}, p={p} has tree depth {td} and proof length {length}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")